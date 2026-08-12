# src/storage/database.py
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from src.config import settings

DB_PATH = settings.BASE_DIR / "data" / "jobs.db"

@dataclass
class JobRecord:
    job_id: str             # ID único da vaga na plataforma (ex: "gupy_123456")
    platform: str           # "gupy", "linkedin", etc.
    title: str
    company: str
    url: str
    description: str
    match_score: Optional[int] = None
    should_apply: Optional[bool] = None
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, APPLIED


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Cria as tabelas necessárias se não existirem."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    platform TEXT NOT NULL,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    url TEXT NOT NULL,
                    description TEXT NOT NULL,
                    match_score INTEGER,
                    should_apply BOOLEAN,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def is_job_processed(self, job_id: str) -> bool:
        """Verifica se a vaga já foi raspada anteriormente."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,))
            return cursor.fetchone() is not None

    def save_job(self, job: JobRecord) -> bool:
        """Insere ou atualiza o registro de uma vaga."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO jobs (job_id, platform, title, company, url, description, match_score, should_apply, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    match_score = excluded.match_score,
                    should_apply = excluded.should_apply,
                    status = excluded.status
            """, (
                job.job_id, job.platform, job.title, job.company, 
                job.url, job.description, job.match_score, 
                job.should_apply, job.status
            ))
            conn.commit()
            return True


if __name__ == "__main__":
    print("=== TESTANDO BANCO DE DADOS LOCAL (SQLite) ===")
    db = Database()
    
    # Teste de salvamento
    sample_job = JobRecord(
        job_id="gupy_99999",
        platform="gupy",
        title="Desenvolvedor Python",
        company="Tech Corp",
        url="https://vaga.gupy.io/99999",
        description="Vaga de teste de integração.",
        match_score=95,
        should_apply=True,
        status="APPROVED"
    )
    
    db.save_job(sample_job)
    print(f"Vaga 'gupy_99999' já existe no banco? {db.is_job_processed('gupy_99999')}")
    print(f"Vaga 'gupy_00000' já existe no banco? {db.is_job_processed('gupy_00000')}")