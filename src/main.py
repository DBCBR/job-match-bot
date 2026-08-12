# src/main.py
import asyncio
import logging
from src.config import settings
from src.evaluator.pdf_reader import extract_text_from_pdf
from src.evaluator.matcher import evaluate_job_match
from src.scrapers.linkedin_scraper import LinkedInScraper
from src.storage.database import Database, JobRecord
from src.notifier.telegram import send_telegram_alert

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("JobMatchBot")


async def run_pipeline(cv_text: str, search_keyword: str, job_limit: int = 10):
    """Executa o pipeline de busca, filtro de IA e armazenamento para um termo específico."""
    db = Database()
    scraper = LinkedInScraper()

    logger.info(f"\n🔍 Iniciando busca para: '{search_keyword}' (Limite: {job_limit})")
    raw_jobs = await scraper.fetch_jobs(keyword=search_keyword, limit=job_limit)

    if not raw_jobs:
        logger.warning(f"Nenhuma vaga recente encontrada para '{search_keyword}'.")
        return

    for i, job_data in enumerate(raw_jobs, 1):
        job_id = job_data["job_id"]
        title = job_data["title"]
        company = job_data["company"]

        logger.info(f"\n--- Processando [{i}/{len(raw_jobs)}]: {title} na empresa {company} ---")

        # Verifica desduplicação no SQLite
        if db.is_job_processed(job_id):
            logger.info(f"Vaga '{job_id}' já consta no banco de dados. Pulando...")
            continue

        try:
            logger.info("Enviando vaga para análise do Gemini...")
            evaluation = evaluate_job_match(
                cv_text=cv_text,
                job_title=title,
                job_description=job_data["description"]
            )

            status = "APPROVED" if evaluation.should_apply else "REJECTED"

            job_record = JobRecord(
                job_id=job_id,
                platform=job_data["platform"],
                title=title,
                company=company,
                url=job_data["url"],
                description=job_data["description"],
                match_score=evaluation.match_score,
                should_apply=evaluation.should_apply,
                status=status
            )

            # Salva no banco local
            db.save_job(job_record)

            logger.info(
                f"Resultado: Score = {evaluation.match_score}/100 | "
                f"Status = {status} | Match Skills = {len(evaluation.matching_skills)}"
            )

            # Dispara alerta no Telegram apenas para vagas aprovadas
            if evaluation.should_apply:
                await send_telegram_alert(
                    title=title,
                    company=company,
                    match_score=evaluation.match_score,
                    url=job_data["url"],
                    matching_skills=evaluation.matching_skills,
                    reasoning=evaluation.summary_reasoning
                )

        except Exception as e:
            logger.error(f"Erro ao processar vaga {job_id}: {e}")


async def main():
    logger.info("=== INICIANDO PIPELINE JOB-MATCH-BOT ===")

    # 1. Carrega o CV apenas uma vez para otimizar a execução
    logger.info(f"Lendo currículo de: {settings.CV_PATH}")
    cv_text = extract_text_from_pdf()

    if not cv_text:
        logger.error("Erro: O conteúdo extraído do CV está vazio. Abortando.")
        return

    # 2. Palavras-chave cobrindo suas áreas de atuação e formação
    keywords = [
        "Desenvolvedor Backend Junior",
        "FastAPI",
        "Python Developer",
        "QA Automation Engineer",
        "Analista de Automação de Testes",
        "Engenheiro de Prompt",
        "Estágio Ciência da Computação",
        "Estágio Backend",
        "Desenvolvedor Java Junior",
        "C++ Developer"
    ]

    # 3. Varre termo por termo
    for kw in keywords:
        await run_pipeline(cv_text=cv_text, search_keyword=kw, job_limit=10)

    logger.info("\n=== PIPELINE CONCLUÍDO COM SUCESSO ===")


if __name__ == "__main__":
    asyncio.run(main())