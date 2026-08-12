# src/scrapers/gupy_scraper.py
import logging
import asyncio
from typing import List, Dict, Any
from playwright.async_api import async_playwright
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class GupyScraper(BaseScraper):
    SEARCH_URL = "https://portal.gupy.io/vagas"

    async def fetch_jobs(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Acessa o portal da Gupy via Playwright e intercepta a resposta da API interna /api/v1/jobs.
        """
        jobs: List[Dict[str, Any]] = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()

            # Evento para capturar a resposta JSON da API oficial de vagas
            async def handle_response(response):
                if "/api/v1/jobs" in response.url and response.status == 200:
                    try:
                        data = await response.json()
                        raw_list = data.get("data", [])
                        for item in raw_list:
                            job_id_raw = item.get("id")
                            if not job_id_raw:
                                continue

                            job_id = f"gupy_{job_id_raw}"
                            title = item.get("name") or "Título não informado"
                            company = item.get("careerPageName") or "Empresa na Gupy"
                            
                            # Trata URL da vaga
                            job_url = item.get("jobUrl") or f"https://portal.gupy.io/job/{job_id_raw}"
                            
                            description = (
                                item.get("description")
                                or item.get("summary")
                                or f"Vaga para {title} na empresa {company}."
                            )

                            jobs.append({
                                "job_id": job_id,
                                "platform": "gupy",
                                "title": title,
                                "company": company,
                                "url": job_url,
                                "description": description,
                                "type": item.get("type", "N/A"),
                                "is_remote": item.get("isRemoteWork", False),
                            })
                    except Exception as e:
                        logger.debug(f"[GupyScraper] Erro ao parsear JSON interceptado: {e}")

            # Registra o interceptador de respostas de rede
            page.on("response", handle_response)

            target_url = f"{self.SEARCH_URL}?searchTerm={keyword}"
            logger.info(f"[GupyScraper] Navegando até {target_url}...")

            try:
                # Navega e aguarda que as requisições de rede sejam concluídas
                await page.goto(target_url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(3000)  # Tempo adicional para garantir a execução do callback
            except Exception as e:
                logger.warning(f"[GupyScraper] Aviso de tempo limite durante o carregamento: {e}")

            await browser.close()

            # Limita a quantidade de vagas capturadas
            limited_jobs = jobs[:limit]
            logger.info(f"[GupyScraper] {len(limited_jobs)} vagas capturadas com sucesso.")
            return limited_jobs


if __name__ == "__main__":
    async def test_scraper():
        print("=== TESTANDO SCRAPER DA GUPY (INTERCEPTOR DE API / PLAYWRIGHT) ===")
        scraper = GupyScraper()
        
        termo = "Python"
        print(f"Buscando vagas para: '{termo}'...")
        
        vagas = await scraper.fetch_jobs(keyword=termo, limit=5)
        
        print(f"\nTotal de vagas retornadas: {len(vagas)}\n")
        for i, vaga in enumerate(vagas, 1):
            print(f"{i}. [{vaga['company']}] {vaga['title']}")
            print(f"   ID: {vaga['job_id']}")
            print(f"   Remoto: {vaga['is_remote']}")
            print(f"   URL: {vaga['url']}\n")

    asyncio.run(test_scraper())