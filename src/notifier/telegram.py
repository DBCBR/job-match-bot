# src/notifier/telegram.py
import logging
import httpx
from src.config import settings

logger = logging.getLogger(__name__)


async def send_telegram_alert(
    title: str,
    company: str,
    match_score: int,
    url: str,
    matching_skills: list[str],
    reasoning: str
) -> bool:
    """
    Envia uma notificação formatada em HTML para o seu Telegram sobre uma vaga aprovada.
    """
    bot_token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)

    if not bot_token or not chat_id:
        logger.warning("[TelegramNotifier] Token ou Chat ID não configurados no .env. Pulando alerta.")
        return False

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Formatação do texto em HTML do Telegram
    skills_str = ", ".join(matching_skills) if matching_skills else "Geral"
    
    message_text = (
        f"🎯 <b>NOVA VAGA APROVADA ({match_score}/100)</b>\n\n"
        f"💼 <b>Vaga:</b> {title}\n"
        f"🏢 <b>Empresa:</b> {company}\n"
        f"✅ <b>Match:</b> {skills_str}\n\n"
        f"📝 <b>Parecer da IA:</b>\n<i>{reasoning}</i>\n\n"
        f"🔗 <a href='{url}'>Clique aqui para se candidatar</a>"
    )

    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(api_url, json=payload)
            response.raise_for_status()
            logger.info(f"[TelegramNotifier] Alerta enviado com sucesso para a vaga '{title}'.")
            return True
        except Exception as e:
            logger.error(f"[TelegramNotifier] Erro ao enviar mensagem para o Telegram: {e}")
            return False