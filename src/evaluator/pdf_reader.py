from pathlib import Path
import pdfplumber
from src.config import settings

def extract_text_from_pdf(pdf_path: Path = None) -> str:
    """
    Extrai e limpa o texto de um arquivo PDF.
    Caso nenhum caminho seja informado, usa o caminho padrão configurado no settings.
    """
    target_path = pdf_path or settings.CV_PATH
    
    if not target_path.exists():
        raise FileNotFoundError(
            f"Arquivo de CV não encontrado no caminho: {target_path}\n"
            "Certifique-se de colocar seu arquivo 'cv.pdf' na pasta 'data/'."
        )
        
    extracted_text = []
    
    with pdfplumber.open(target_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                extracted_text.append(text)
            else:
                print(f"[AVISO] Não foi possível extrair texto da página {page_number}.")
                
    full_text = "\n".join(extracted_text)
    
    # Sanitização básica do texto extraído
    cleaned_text = "\n".join(
        [line.strip() for line in full_text.splitlines() if line.strip()]
    )
    
    return cleaned_text

if __name__ == "__main__":
    # Teste rápido do extrator
    try:
        cv_content = extract_text_from_pdf()
        print("=== TEXTO EXTRAÍDO DO CV COM SUCESSO ===")
        print(cv_content[:500])  # Imprime os primeiros 500 caracteres
        print("\n...")
    except Exception as e:
        print(f"Erro ao ler o CV: {e}")