# src/scrapers/linkedin_scraper.py
import logging
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class LinkedInScraper(BaseScraper):
    """
    Scraper otimizado para vagas recentes (últimas 24h) em modelo Remoto ou Híbrido no RJ.
    """

    GUEST_API_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    async def fetch_jobs(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        start = 0

        async with httpx.AsyncClient(headers=self.headers, follow_redirects=True, timeout=15.0) as client:
            while len(jobs) < limit:
                params = {
                    "keywords": keyword,
                    "location": "Rio de Janeiro, Brazil",
                    "f_TPR": "r86400",  # Publicadas nas últimas 24 horas
                    "f_WT": "2,3",      # 2 = Remoto, 3 = Híbrido
                    "start": start,
                }

                try:
                    logger.info(f"[LinkedInScraper] Buscando vagas 24h (Remoto/Híbrido RJ) para '{keyword}'...")
                    response = await client.get(self.GUEST_API_URL, params=params)

                    if response.status_code != 200:
                        logger.warning(f"[LinkedInScraper] Status {response.status_code}. Interrompendo.")
                        break

                    soup = BeautifulSoup(response.text, "html.parser")
                    job_cards = soup.find_all("li")

                    if not job_cards:
                        logger.info("[LinkedInScraper] Nenhuma vaga nova encontrada nas últimas 24h.")
                        break

                    for card in job_cards:
                        if len(jobs) >= limit:
                            break

                        link_elem = card.find("a", class_="base-card__full-link") or card.find("a")
                        if not link_elem or not link_elem.get("href"):
                            continue

                        full_url = link_elem["href"].split("?")[0]
                        job_id_raw = full_url.rstrip("/").split("-")[-1]
                        job_id = f"linkedin_{job_id_raw}"

                        title_elem = card.find("h3", class_="base-search-card__title")
                        title = title_elem.get_text(strip=True) if title_elem else "Título não informado"

                        company_elem = card.find("h4", class_="base-search-card__subtitle")
                        company = company_elem.get_text(strip=True) if company_elem else "Empresa não informada"

                        location_elem = card.find("span", class_="job-search-card__location")
                        location = location_elem.get_text(strip=True) if location_elem else "Rio de Janeiro"

                        # Captura tempo de publicação amigável (ex: "Há 2 horas", "Há 10 minutos")
                        time_elem = card.find("time")
                        posted_time = time_elem.get_text(strip=True) if time_elem else "Recente (24h)"

                        description = f"Vaga: {title} na empresa {company}. Local: {location}. Publicada: {posted_time}. Link: {full_url}"

                        jobs.append({
                            "job_id": job_id,
                            "platform": "linkedin",
                            "title": title,
                            "company": company,
                            "url": full_url,
                            "description": description,
                            "posted_time": posted_time,
                            "type": "Efetivo/Geral",
                            "is_remote": "remoto" in location.lower() or "home office" in location.lower(),
                        })

                    start += 25

                except Exception as exc:
                    logger.error(f"[LinkedInScraper] Erro ao raspar LinkedIn: {exc}")
                    break

        logger.info(f"[LinkedInScraper] {len(jobs)} vagas hiper-recentes encontradas.")
        return jobs


if __name__ == "__main__":
    import asyncio

    async def test_scraper():
        print("=== TESTANDO FILTRO 24H + REMOTO/HÍBRIDO RJ ===")
        scraper = LinkedInScraper()
        vagas = await scraper.fetch_jobs(keyword="Python", limit=5)
        
        print(f"\nTotal de vagas retornadas: {len(vagas)}\n")
        for i, vaga in enumerate(vagas, 1):
            print(f"{i}. [{vaga['company']}] {vaga['title']}")
            print(f"   Publicada: {vaga['posted_time']}")
            print(f"   URL: {vaga['url']}\n")

    asyncio.run(test_scraper())