# 🤖 Job Match Bot

```
                    +----------------------+
                    |   Currículo (PDF)    |
                    +----------+-----------+
                               |
                               v

```

+------------------+    +----------------------+    +-----------------------+
|  LinkedIn Guest  | -> |  LinkedInScraper     | -> |  Evaluator (Gemini)   |
|  API (24h / RJ)  |    |  (httpx + BS4)       |    |  (Structured JSON)    |
+------------------+    +----------------------+    +-----------+-----------+
|
v
+------------------+    +----------------------+    +-----------------------+
|  Telegram Bot    | <- |  Database (SQLite)   | <- |  Match Score >= 80%   |
|  (Notifier HTML) |    |  (Deduplication)     |    |  (Decision Engine)    |
+------------------+    +----------------------+    +-----------------------+

```

### Stack Técnica:
* **Linguagem & Runtime:** Python 3.10+
* **Inteligência Artificial:** Google GenAI SDK (`gemini-3.5-flash-lite`), Pydantic Schema Validation
* **Web Scraping & Parsing:** `httpx`, `BeautifulSoup4`, `Playwright`
* **Banco de Dados:** SQLite3 com `pydantic` / `dataclasses`
* **Agendamento & Automação:** `APScheduler`
* **Notificações:** Telegram Bot API (HTML sanitizado via `html.escape`)

---

## ⚙️ Funcionalidades Principais

* [x] **Parsing Automático de PDF:** Extração do texto do currículo do candidato.
* [x] **Coleta Filtrada de Vagas:** Integração com a API Guest do LinkedIn aplicando filtros de tempo (24h) e localidade (Remoto/Híbrido).
* [x] **Análise Aprofundada por IA:** Avaliação de aderência técnica, extração de *matching skills*, *missing skills* e parecer técnico sucinto.
* [x] **Camada de Persistência:** Gravação histórica das vagas com status `APPROVED` ou `REJECTED`.
* [x] **Notificações Instantâneas:** Envio de relatórios visuais no Telegram com link direto para candidatura.
* [x] **Agendador Diário:** Suporte a execuções automáticas via Cron/APScheduler.

---

## 🚀 Como Executar o Projeto

### Pró-requisitos
* Python 3.10 ou superior instalado
* Chave de API do Google Gemini (`GEMINI_API_KEY`)
* Token de Bot e Chat ID do Telegram (para alertas)

### 1. Clonar o Repositório e Criar Ambiente Virtual
```bash
git clone [https://github.com/DBCBR/job-match-bot.git](https://github.com/DBCBR/job-match-bot.git)
cd job-match-bot

python -m venv .venv
# No Windows PowerShell:
.\.venv\Scripts\Activate.ps1

```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt

```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto contendo:

```env
GEMINI_API_KEY=sua_gemini_api_key
TELEGRAM_BOT_TOKEN=seu_bot_token
TELEGRAM_CHAT_ID=seu_chat_id
LOG_LEVEL=INFO
MIN_MATCH_SCORE=80

```

Adicione seu currículo em formato PDF no caminho: `data/cv.pdf`.

### 4. Executar a Aplicação

**Modo Manual (Varredura Imadiata):**

```bash
python -m src.main

```

**Modo Agendado (Rotina Diária):**

```bash
python -m src.scheduler

```

---

## 📊 Estrutura do Repositório

```text
job-match-bot/
├── data/
│   ├── cv.pdf               # Currículo do candidato
│   └── jobs.db              # Banco SQLite de vagas
├── src/
│   ├── config.py            # Validação de ambiente (Pydantic Settings)
│   ├── evaluator/
│   │   ├── matcher.py       # Integração com Gemini API e Prompts de IA
│   │   └── pdf_reader.py    # Extrator de texto de PDF
│   ├── notifier/
│   │   └── telegram.py      # Notificador Telegram via Webhook/API
│   ├── scrapers/
│   │   ├── base.py          # Classe base abstrata (BaseScraper)
│   │   └── linkedin_scraper.py # Scraper da API pública do LinkedIn
│   ├── storage/
│   │   └── database.py      # Camada DAO/SQLite de desduplicação
│   ├── main.py              # Pipeline principal (Execução sob demanda)
│   └── scheduler.py         # Agendador de tarefas diárias
├── .env.example             # Modelo de variáveis de ambiente
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação técnica

```

---

## 👤 Autor

**David Barcellos Cardoso**

* **LinkedIn:** [linkedin.com/in/david-barcellos-cardoso](https://www.google.com/search?q=https://linkedin.com/in/david-barcellos-cardoso/)
* **GitHub:** [github.com/DBCBR](https://www.google.com/search?q=https://github.com/DBCBR)
