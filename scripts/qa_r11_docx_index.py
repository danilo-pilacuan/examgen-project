"""BUG-029 verification: retry docx indexing via API and compare chunk counts."""
import json
import urllib.request

BASE = "http://localhost:8000"
SUBJECT = "6c9e3cc3-6599-4868-a8a4-685bbb12bc30"


def post_index(materials: list[str], clear: bool = True) -> None:
    body = json.dumps({"materials": materials, "clear": clear}).encode()
    req = urllib.request.Request(
        f"{BASE}/subjects/{SUBJECT}/index",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            print("HTTP", r.status, r.read().decode())
    except Exception as e:  # noqa: BLE001
        print("ERR", type(e).__name__, e)


def count_chunks() -> int:
    import psycopg

    with psycopg.connect(
        "host=localhost port=5432 user=exam_user password=exam_password dbname=exam_generator_db"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT count(*) FROM material_chunks WHERE subject_id = %s", (SUBJECT,)
            )
            return cur.fetchone()[0]


if __name__ == "__main__":
    print("chunks before:", count_chunks())
    post_index(["/app/inputs/Economia_Aplicada/Apuntes/*.docx"])
    print("chunks after docx:", count_chunks())
    post_index(["/app/inputs/Economia_Aplicada/Apuntes/*.pptx"])
    print("chunks after pptx:", count_chunks())
