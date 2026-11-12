#!/usr/bin/env python3
"""Bring-up entrypoint: exam-generator from a fresh clone.

Implements RECIPE.md steps 1-5 plus a post-smoke submodule pin check
(step 6): clone submodules, write .env (asks for the LLM API key,
generates AUTH_SECRET), build + start the Docker stack, run smoke checks,
expose the system via a cloudflared quick tunnel and print the public URL.

Standard library only (Python 3.7+). Needs git and docker in PATH.
Optional: OPENAI_API_KEY in the environment skips the interactive prompt.

Usage:
    python scripts/bring-up.py
    OPENAI_API_KEY=sk-... python scripts/bring-up.py
    python scripts/bring-up.py --no-tunnel
    python scripts/bring-up.py --reuse-running   # adopt a foreign running
                                                 # stack as-is (RECIPE 0A-3)

Refuses to rebuild when running exam_* containers belong to another
checkout; use --reuse-running to adopt them as-is (smoke + tunnel only).
Idempotent; safe to re-run. No secrets are echoed or stored anywhere but
the gitignored .env.
"""

import argparse
import getpass
import os
import re
import secrets
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPOSE_FILE = os.path.join("docker", "docker-compose.yml")
HEALTH_TIMEOUT_S = 600
TUNNEL_TIMEOUT_S = 120
PLACEHOLDERS = ("", "sk-xxxx", "__REPLACE_ME__")
TOTAL = 5


def log(msg):
    print(msg, flush=True)


def fail(msg):
    print("ERROR: %s" % msg, file=sys.stderr, flush=True)
    sys.exit(1)


def init_console():
    # Never crash printing on legacy consoles (cp1252, etc.).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass


def sh(cmd, check=True, capture=False):
    """Run a command; inherits the console unless capture=True."""
    kw = {}
    if capture:
        kw = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            "errors": "replace",
        }
    result = subprocess.run(cmd, **kw)
    if check and result.returncode != 0:
        fail("command failed (%d): %s" % (result.returncode, " ".join(cmd)))
    return result


def step_header(n, text):
    log("==> [%d/%d] %s" % (n, TOTAL, text))


# --- .env helpers (byte-level: encoding and line endings stay untouched) ---

def get_dotenv_value(path, key):
    with open(path, "rb") as f:
        data = f.read()
    m = re.search(rb"(?m)^" + key.encode() + rb"=([^\r\n]*)", data)
    if not m:
        return ""
    return m.group(1).decode("utf-8", "replace").strip()


def set_dotenv_value(path, key, value):
    with open(path, "rb") as f:
        data = f.read()
    pattern = re.compile(rb"(?m)^(" + key.encode() + rb"=)[^\r\n]*")
    new_data, n = pattern.subn(lambda m: m.group(1) + value.encode(), data, count=1)
    if n == 0:
        sep = b"\r\n" if b"\r\n" in data else b"\n"
        head = data if data.endswith(b"\n") else data + sep
        new_data = head + key.encode() + b"=" + value.encode() + sep
    with open(path, "wb") as f:
        f.write(new_data)


# --- steps ---

def preflight():
    if not shutil.which("git"):
        fail("git not found in PATH (install it from https://git-scm.com)")
    if not shutil.which("docker"):
        fail("docker not found in PATH (start Docker Desktop first)")
    r = sh(["docker", "compose", "version"], check=False, capture=True)
    if r.returncode != 0:
        fail("docker compose (v2) not available; update Docker Desktop")


# --- running-stack detection (RECIPE section 0A rule 3) ---

STACK_SERVICES = ("exam_app", "exam_frontend", "exam_postgres_db",
                  "exam_latex_compiler", "exam_embedding_service")


def inspect_container(name):
    """Return (state, config_files_label) or (None, None) if absent."""
    r = sh(["docker", "inspect", "--format",
            "{{.State.Status}}|{{index .Config.Labels"
            " \"com.docker.compose.project.config_files\"}}", name],
           check=False, capture=True)
    if r.returncode != 0:
        return None, None
    out = r.stdout.strip()
    state, _, cfg = out.partition("|")
    return (state or None), (cfg or None)


def running_stack_state():
    """Classify running exam_* containers.

    Returns (count_up, owner_config_files) where owner_config_files is the
    com.docker.compose.project.config_files label shared by the up
    containers, or None when absent or inconsistent.
    """
    count = 0
    owners = set()
    for name in STACK_SERVICES:
        state, cfg = inspect_container(name)
        if state in ("running", "restarting"):
            count += 1
            if cfg:
                owners.add(cfg)
    if len(owners) > 1:
        return count, "INCONSISTENT"
    return count, (next(iter(owners)) if owners else None)


def running_stack_is_ours():
    count, owner = running_stack_state()
    if count == 0:
        return False
    if owner and os.path.normcase(os.path.abspath(
            os.path.dirname(owner))) == os.path.normcase(
            os.path.abspath(os.path.join(ROOT, "docker"))):
        return True
    return False


def normalize_owner_path(owner):
    """Return the checkout root implied by a config_files label, or None."""
    if not owner or owner == "INCONSISTENT":
        return None
    return os.path.dirname(os.path.abspath(owner))


def step1_submodules():
    step_header(1, "Cloning submodules (pinned SHAs)")
    sh(["git", "submodule", "update", "--init", "--recursive"])


def step2_secrets():
    step_header(2, "Secrets (.env)")
    env_path = os.path.join(ROOT, ".env")
    example = os.path.join(ROOT, ".env.example")
    if not os.path.isfile(env_path):
        shutil.copyfile(example, env_path)
        set_dotenv_value(env_path, "OPENAI_API_KEY", "__REPLACE_ME__")
        log("    .env created from .env.example")
    key = get_dotenv_value(env_path, "OPENAI_API_KEY")
    if key in PLACEHOLDERS:
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if key:
            log("    Taking OPENAI_API_KEY from environment")
        elif sys.stdin.isatty():
            key = getpass.getpass(
                "    Enter your LLM gateway API key (input hidden): ").strip()
        else:
            fail("OPENAI_API_KEY missing: set the env var OPENAI_API_KEY "
                 "or run the script in an interactive terminal")
        if not key:
            fail("OPENAI_API_KEY is required (LLM gateway)")
        set_dotenv_value(env_path, "OPENAI_API_KEY", key)
    auth = get_dotenv_value(env_path, "AUTH_SECRET")
    if not auth:
        set_dotenv_value(env_path, "AUTH_SECRET", secrets.token_hex(48))
        log("    AUTH_SECRET generated (48 random bytes)")
    log("    .env ready (gitignored)")


def step3_stack(args):
    step_header(3, "Building and starting containers (5-10 min first time)")
    count, owner = running_stack_state()
    if count and not running_stack_is_ours():
        other = normalize_owner_path(owner)
        if args.reuse_running:
            log("    Stack already running from %s; reusing it as-is "
                "(--reuse-running)" % (other or "an unknown checkout"))
            return
        msg = ("%d exam_* container(s) already running from another "
               "checkout" % count)
        if other:
            msg += " (%s)" % other
        msg += ("; refusing to touch them. Re-run with --reuse-running to"
                " adopt the running stack as-is, or stop it first from its"
                " own checkout: docker compose -f docker/docker-compose.yml"
                " down")
        fail(msg)
    if count:
        log("    Stack already running from this checkout; "
            "refreshing with compose up")
    # A nonzero exit here can be cosmetic on some shells; health + smoke
    # checks below are the source of truth.
    sh(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d", "--build"],
       check=False)
    log("    Waiting for exam_app to become healthy")
    waited = 0
    while waited < HEALTH_TIMEOUT_S:
        r = sh(["docker", "inspect", "--format",
                "{{.State.Health.Status}}", "exam_app"],
               check=False, capture=True)
        if r.stdout.strip() == "healthy":
            log("    exam_app healthy")
            return
        time.sleep(5)
        waited += 5
    fail("exam_app not healthy after 10 min (try: docker logs exam_app)")


def http_status(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


def step4_smoke():
    step_header(4, "Smoke checks")
    try:
        code = http_status("http://localhost:3000/")
        if code != 200:
            fail("frontend / returned %d (expected 200)" % code)
        log("    SPA 200")
        code = http_status("http://localhost:3000/subjects",
                           {"Accept": "application/json"})
        if code != 401:
            fail("/subjects returned %d without token (expected 401)" % code)
        log("    /subjects 401 without token (auth OK)")
    except urllib.error.URLError as e:
        fail("cannot reach http://localhost:3000 (%s); is the frontend up?"
             % getattr(e, "reason", e))


def step5_tunnel():
    step_header(5, "Public exposure (cloudflared quick tunnel)")
    sh(["docker", "rm", "-f", "exam_tunnel"], check=False, capture=True)
    # exam_tunnel runs inside the compose project (service "tunnel",
    # profile "tunnel") and reaches the SPA by the compose alias
    # exam-frontend; same teardown as the rest of the stack.
    sh(["docker", "compose", "-f", COMPOSE_FILE, "--profile", "tunnel",
        "up", "-d", "tunnel"], check=False)
    url = ""
    deadline = time.time() + TUNNEL_TIMEOUT_S
    while time.time() < deadline:
        r = sh(["docker", "logs", "exam_tunnel"], check=False, capture=True)
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com",
                      (r.stdout or "") + (r.stderr or ""))
        if m:
            url = m.group(0)
            break
        time.sleep(3)
    if not url:
        fail("no trycloudflare URL in exam_tunnel logs after 2 min")
    log("")
    log("=" * 60)
    log("  System is UP and EXPOSED")
    log("  Local:    http://localhost:3000")
    log("  Public:   %s" % url)
    log("  Teardown: docker compose -f docker/docker-compose.yml "
        "--profile tunnel down")
    log("=" * 60)


def step6_submodules():
    step_header(6, "Verifying submodules at pinned SHAs")
    r = sh(["git", "submodule", "status", "--recursive"], check=False,
           capture=True)
    if r.returncode != 0:
        fail("git submodule status failed: %s" % (r.stderr or "").strip())
    lines = [ln for ln in (r.stdout or "").splitlines() if ln.strip()]
    if not lines:
        fail("git submodule status listed 0 submodules (expected 6); "
             "run: git submodule update --init --recursive")
    bad = []
    for ln in lines:
        flag, sha_path = ln[0], ln[1:].strip()
        path = sha_path.split()[0] if sha_path else "?"
        if flag == "+":
            bad.append("- %s: checked out at a different SHA than pinned; "
                       "fix: git submodule update --init --recursive" % path)
        elif flag == "U":
            bad.append("- %s: has merge conflicts; resolve them or run: "
                       "git submodule update --init --recursive" % path)
        elif flag == "-":
            bad.append("- %s: not initialized; fix: git submodule update "
                       "--init --recursive" % path)
    if bad:
        fail("submodules are not at their pinned state:\n" + "\n".join(bad))
    log("    %d submodules OK (no +, - or U flags)" % len(lines))


def main():
    global TOTAL
    init_console()
    parser = argparse.ArgumentParser(
        description="Bring up the exam-generator stack and expose it "
                    "via a cloudflared quick tunnel (RECIPE.md)")
    parser.add_argument("--no-tunnel", action="store_true",
                        help="skip the public cloudflared tunnel")
    parser.add_argument("--reuse-running", action="store_true",
                        help="adopt an already-running exam_* stack from "
                             "another checkout as-is (RECIPE section 0A "
                             "rule 3); no rebuild, no restart")
    args = parser.parse_args()
    TOTAL = 4 if args.no_tunnel else 5

    os.chdir(ROOT)
    log("==> Repo root: %s" % ROOT)
    preflight()
    step1_submodules()
    step2_secrets()
    step3_stack(args)
    step4_smoke()
    step6_submodules()
    if args.no_tunnel:
        log("")
        log("System is UP (local only). Teardown: "
            "docker compose -f docker/docker-compose.yml down")
        return
    step5_tunnel()

if __name__ == "__main__":
    main()
