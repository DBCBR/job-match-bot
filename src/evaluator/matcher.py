# src/evaluator/matcher.py
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from src.config import settings

logger = logging.getLogger(__name__)

class JobEvaluation(BaseModel):
    match_score: int = Field(description="Nota de 0 a 100 indicando a compatibilidade.")
    should_apply: bool = Field(description="True se o score for >= 80 e o candidato for elegível.")
    matching_skills: list[str] = Field(description="Habilidades do CV encontradas na vaga.")
    missing_skills: list[str] = Field(description="Requisitos exigidos na vaga que faltam no CV.")
    summary_reasoning: str = Field(description="Resumo sucinto justificando a pontuação.")


def evaluate_job_match(cv_text: str, job_title: str, job_description: str) -> JobEvaluation:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # REGRAS RÍGIDAS DE FILTRAGEM ADICIONADAS AQUI:
    system_instructions = (
        "Você é um recrutador técnico e estrategista de carreira. Avalie a aderência do Currículo à Vaga.\n\n"
        "REGRAS OBRIGATÓRIAS DE DESCARTE:\n"
        "1. FILTRO DE CONCORRÊNCIA: Se a descrição mencionar que a vaga possui mais de 50 ou 100 candidaturas ("
        "ou 'alta concorrência'), REJEITE a vaga (should_apply = False, match_score < 70).\n"
        "2. FILTRO DE LOCALIZAÇÃO: Se a vaga for estritamente PRESENCIAL fora da capital do Rio de Janeiro, "
        "REJEITE a vaga (deve ser Remoto ou Híbrido no RJ).\n"
        "3. AVALIAÇÃO TÉCNICA: Considere o perfil de Backend (Python, FastAPI, C++, Java), QA Automation (Selenium, Pytest) e "
        "GenAI/Dados. Se a vaga pedir senioridade Sênior/Especialista (exige 5+ anos), penalize o score por não ser o foco do perfil (Júnior/Estágio/Pleno).\n"
        f"4. Defina should_apply = True APENAS se match_score >= {settings.MIN_MATCH_SCORE} e passar em todos os filtros acima."
    )

    prompt = f"""
    {system_instructions}

    --- TÍTULO DA VAGA ---
    {job_title}

    --- DESCRIÇÃO DA VAGA ---
    {job_description}

    --- CURRÍCULO DO CANDIDATO ---
    {cv_text}
    """

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JobEvaluation,
                temperature=0.2,
            ),
        )

        evaluation = JobEvaluation.model_validate_json(response.text)
        return evaluation

    except Exception as e:
        logger.error(f"Erro ao avaliar vaga '{job_title}' com Gemini: {e}")
        raise e


if __name__ == "__main__":
    from src.evaluator.pdf_reader import extract_text_from_pdf

    print(f"=== TESTANDO AVALIADOR COM GEMINI ({settings.GEMINI_MODEL}) ===")
    
    sample_title = "Desenvolvedor Backend Python Júnior"
    sample_description = """
    Vaga 100% Remota. Publicada há 2 horas (12 candidaturas).
    Buscamos Desenvolvedor Backend com domínio em Python, FastAPI, SQL, Git e Docker.
    """

    try:
        cv_content = extract_text_from_pdf()
        result = evaluate_job_match(cv_content, sample_title, sample_description)
        
        print("\n--- RESULTADO DA AVALIAÇÃO ---")
        print(f"Score: {result.match_score}/100")
        print(f"Deve se candidatar? {'SIM' if result.should_apply else 'NÃO'}")
        print(f"Habilidades Encontradas: {', '.join(result.matching_skills)}")
        print(f"Habilidades Faltantes: {', '.join(result.missing_skills)}")
        print(f"Justificativa: {result.summary_reasoning}")

    except Exception as err:
        print(f"Falha no teste: {err}")