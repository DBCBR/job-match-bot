# src/scheduler.py
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.config import settings
from src.main import run_pipeline

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("JobMatchScheduler")

# Lista estratégica de termos baseada no seu CV (Backend, QA, GenAI e Estágio)
KEYWORDS = [
    # 1. Backend & Desenvolvimento Geral
    "Desenvolvedor Backend Junior",
    "Python Backend Developer",
    "FastAPI Developer",
    "Desenvolvedor Java Junior",
    "C++ Developer",

    # 2. QA, Automação & Testes
    "QA Automation Engineer",
    "Analista de Automação de Testes",
    "QA Tester Junior",

    # 3. GenAI, Automação & Dados
    "Engenheiro de Prompt",
    "Python Automation Developer",
    "Engenheiro de Dados Junior",

    # 4. Estágios (Alta aderência ao seu curso de Ciência da Computação)
    "Estágio Ciência da Computação",
    "Estágio Desenvolvimento Backend",
    "Estágio QA Automação"
]


async def daily_job_search():
    logger.info("⏰ Executando rotina diária expandida de varredura...")
    for kw in KEYWORDS:
        logger.info(f"\n🔍 Buscando oportunidades para: '{kw}'")
        # Limite de 10 vagas por termo (140 vagas analisadas por dia)
        await run_pipeline(search_keyword=kw, job_limit=10)
    logger.info("✅ Rotina diária concluída com sucesso!")


async def main():
    scheduler = AsyncIOScheduler()

    # Agenda a execução diária para às 08:30 AM
    scheduler.add_job(
        daily_job_search,
        trigger="cron",
        hour=8,
        minute=30,
        id="daily_job_search",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("🚀 Agendador iniciado! O robô varrerá 14 áreas do seu perfil todos os dias às 08:30.")

    # Executa a varredura imediata ao subir o serviço
    await daily_job_search()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Agendador encerrado.")