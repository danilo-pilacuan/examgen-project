import sys

sys.path.insert(0, ".")
from sqlalchemy import text

from core.domain.models import Subject
from core.infrastructure.db.connection import SessionLocal

db = SessionLocal()
sid = db.execute(text("SELECT id FROM subjects WHERE name LIKE '%Eva%'")).scalar()
db.close()
print("subject_id:", sid)

from agents_backend.shared.retrieval import retrieve_chunks

chunks = retrieve_chunks(query="Estudio de Mercado", subject_id=str(sid), top_k=3, min_score=0.15)
print("chunks retrieved:", len(chunks))
for c in chunks:
    print(" score:", round(c["score"], 3), "|", c["content"][:60].replace("\n", " "))
