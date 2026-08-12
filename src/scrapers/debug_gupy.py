# src/scrapers/debug_gupy.py
import asyncio
import json
import httpx
from bs4 import BeautifulSoup

async def debug_gupy():
    url = "https://portal.gupy.io/vagas?searchTerm=Python"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        
        if script and script.string:
            data = json.loads(script.string)
            print("=== ESTRUTURA DO NEXT_DATA ENCONTRADA ===")
            page_props = data.get("props", {}).get("pageProps", {})
            print("Chaves dentro de pageProps:", list(page_props.keys()))
            
            # Salva o JSON completo em um arquivo para análise
            with open("gupy_debug.json", "w", encoding="utf-8") as f:
                json.dump(page_props, f, ensure_ascii=False, indent=2)
            print("\n Payload salvo com sucesso em 'gupy_debug.json'!")
        else:
            print(" Tag __NEXT_DATA__ não foi encontrada.")

if __name__ == "__main__":
    asyncio.run(debug_gupy())