# 🤖 Job Match Bot

---

## 🧠 Engenharia de Prompt & Decisões de Arquitetura

### 1. Extensibilidade de Scrapers (Adapter Pattern)

A camada de coleta herda de uma classe abstrata `BaseScraper`, permitindo integrar novas plataformas (ex: Gupy, InfoJobs, Catho) padronizando o contrato do dicionário de saída sem alterar o núcleo da aplicação.

### 2. Garantia de Saída Estrita (Pydantic Schema Validation)

Diferente de chamadas puras a LLMs que podem alucinar texto livre, a API do Gemini é configurada com `response_schema=JobEvaluation`. O retorno é parseado e validado estritamente em runtime pelo Pydantic, garantindo tipagem forte nos atributos `match_score`, `matching_skills` e `should_apply`.

### 3. Filtros Rígidos de Negócio no Inferencia Engine

A avaliação pela IA não considera apenas *keywords*. O prompt contém guardrails explícitos:

* **Filtro de Concorrência:** Penalização direta se a descrição indicar volume excessivo de candidatos ($> 50/100$).
* **Filtro Geográfico/Presencialidade:** Descarte imediato de vagas estritamente presenciais fora do hub do candidato.
* **Filtro de Senioridade:** Calibragem focada no perfil de atuação do candidato (Júnior/Pleno/Estágio).

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Python 3.10+
* Chave de API do **Google Gemini**
* Token de Bot e Chat ID do **Telegram**

### Setup Rápido

```bash
# 1. Clonar o repositório
git clone [https://github.com/DBCBR/job-match-bot.git](https://github.com/DBCBR/job-match-bot.git)
cd job-match-bot

# 2. Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

```

### Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
LOG_LEVEL=INFO
MIN_MATCH_SCORE=80

```

> **Nota:** Certifique-se de posicionar o arquivo do seu currículo em `data/cv.pdf`.

### Execução

* **Execução Sob Demanda (Pipeline Manual):**

```bash
python -m src.main

```

* **Execução Agendada (Serviço Background via APScheduler):**

```bash
python -m src.scheduler

```

---

## 📁 Estrutura do Repositório

```text
job-match-bot/
├── data/
│   ├── cv.pdf               # Currículo base do candidato
│   └── jobs.db              # Banco SQLite de persistência histórica
├── src/
│   ├── config.py            # Gestão centralizada de configurações (Pydantic Settings)
│   ├── evaluator/
│   │   ├── matcher.py       # Avaliador de IA com Gemini API e Structured Outputs
│   │   └── pdf_reader.py    # Módulo de extração e higienização de texto de PDF
│   ├── notifier/
│   │   └── telegram.py      # Notificador Telegram com sanitização HTML
│   ├── scrapers/
│   │   ├── base.py          # Interface/Classe abstrata para scrapers
│   │   └── linkedin_scraper.py # Extrator para a Guest API do LinkedIn
│   ├── storage/
│   │   └── database.py      # Camada DAO para desduplicação e SQLite
│   ├── main.py              # Orquestrador assíncrono principal
│   └── scheduler.py         # Agendador de tarefas recorrentes (APScheduler)
├── .env.example             # Template das variáveis de ambiente
├── requirements.txt         # Grafo de dependências do projeto
└── README.md                # Documentação técnica do projeto

```

---

## 👤 Autor

**David Barcellos Cardoso**

*Desenvolvedor Python & Backend | Automação, GenAI & Engenharia de Software*

* **LinkedIn:** [linkedin.com/in/david-barcellos-cardoso](https://www.google.com/search?q=https://linkedin.com/in/david-barcellos-cardoso/)
* **GitHub:** [github.com/DBCBR](https://www.google.com/search?q=https://github.com/DBCBR)

```

```
