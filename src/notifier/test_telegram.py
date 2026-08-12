# src/notifier/test_telegram.py
import asyncio
from src.notifier.telegram import send_telegram_alert

async def main():
    print("=== TESTANDO DISPARO DO TELEGRAM ===")
    success = await send_telegram_alert(
        title="Desenvolvedor Backend Python (Teste)",
        company="Tech Company",
        match_score=90,
        url="https://www.linkedin.com",
        matching_skills=["Python", "FastAPI", "Docker", "SQL"],
        reasoning="Candidato possui excelente aderência técnica com os requisitos de backend."
    )
    if success:
        print(" Mensagem enviada para o Telegram com sucesso!")
    else:
        print(" Falha no envio. Verifique o TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env")

if __name__ == "__main__":
    asyncio.run(main())