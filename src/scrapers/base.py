# src/scrapers/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    """Classe base abstrata para todos os scrapers de vagas."""

    @abstractmethod
    async def fetch_jobs(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca vagas com base em uma palavra-chave.
        Retorna uma lista de dicionários padronizados com os dados da vaga.
        """
        pass