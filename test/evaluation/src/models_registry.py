"""Central multi-provider model registry (loaded from models.yaml).

Every experiment arm references a model *profile* defined in
``test/evaluation/models.yaml``. Adding a new provider (OpenAI, DeepSeek,
Ollama, a private vLLM...) only requires appending an entry to the YAML —
no code changes.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

EVAL_ROOT = Path(__file__).resolve().parent.parent
MODELS_YAML = EVAL_ROOT / "models.yaml"


@dataclass(frozen=True)
class ModelProfile:
    """One configurable LLM profile (real endpoint or offline stub)."""
    name: str
    provider: str
    base_url: str
    api_key: str
    model: str
    mode: str  # "real" | "stub"


def load_registry(path: Path = MODELS_YAML) -> dict[str, ModelProfile]:
    """Loads all model profiles from the registry YAML."""
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    profiles: dict[str, ModelProfile] = {}
    for name, cfg in (raw.get("models") or {}).items():
        key_env = cfg.get("api_key_env") or ""
        profiles[name] = ModelProfile(
            name=name,
            provider=cfg.get("provider", "unknown"),
            base_url=cfg.get("base_url") or "",
            api_key=os.environ.get(key_env, "") if key_env else "",
            model=cfg.get("model", name),
            mode=cfg.get("mode", "real"),
        )
    return profiles


def get_profile(name: str, path: Path = MODELS_YAML) -> ModelProfile:
    """Returns one model profile by logical name."""
    registry = load_registry(path)
    if name not in registry:
        available = ", ".join(sorted(registry))
        raise KeyError(f"Unknown model profile '{name}'. Available: {available}")
    return registry[name]
