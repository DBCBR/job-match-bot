# 🤖 Job Match Bot

---

## 📐 Padrões de Projeto & Decisões Arquiteturais

* **Adapter Pattern (`src/scrapers/`):** Todos os scrapers herdam de `BaseScraper`, permitindo desacoplar a origem dos dados (LinkedIn, Gupy, etc.) do pipeline de avaliação.
* **Data Access Object - DAO (`src/storage/`):** Isolamento da camada de persistência com métodos específicos para verificação de duplicidade (`is_job_processed`) e salvamento (`save_job`).
* **Structured Output Pattern (`src/evaluator/`):** Uso do `response_schema` da API GenAI garantindo validação em tempo de execução via `Pydantic`.
* **Guardrails de Negócio:** Conjunto de regras estritas no prompt para descartar concorrência excessiva ($> 50$ candidaturas), presencialidade fora da capital do RJ e desalinhamento de senioridade.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Inteligência Artificial:** Google GenAI SDK (`gemini-3.5-flash-lite`), Pydantic v2
* **Web Scraping:** `httpx`, `BeautifulSoup4`, `Playwright`
* **Persistência de Dados:** SQLite3, Dataclasses
* **Agendamento & Notificação:** `APScheduler`, Telegram Bot API

---

## ⚙️ Instalação e Execução

### Pré-requisitos

* Python 3.10+
* Chave de API do **Google Gemini**
* Token de Bot e Chat ID do **Telegram**

### 1. Clonar o Repositório e Configurar Ambiente

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
GEMINI_API_KEY=sua_chave_gemini
TELEGRAM_BOT_TOKEN=seu_bot_token
TELEGRAM_CHAT_ID=seu_chat_id
LOG_LEVEL=INFO
MIN_MATCH_SCORE=80

```

> **Importante:** Posicione o seu currículo em formato PDF no diretório `data/cv.pdf`.

### 4. Executar o Pipeline

**Modo Sob Demanda (Busca Manual):**

```bash
python -m src.main

```

**Modo Agendado (Serviço Diário):**

```bash
python -m src.scheduler

```

---

## 🧪 Execução dos Testes

Para garantir a integridade dos módulos de leitura de PDF, banco de dados e enviador do Telegram:

```bash
# Teste de extração de PDF
python -m src.evaluator.pdf_reader

# Teste de banco de dados SQLite
python -m src.storage.database

# Teste de envio de alerta no Telegram
python -m src.notifier.test_telegram

```

---

## 👤 Autor

**David Barcellos Cardoso**

*Desenvolvedor Python & Backend | Automação, GenAI & Engenharia de Software*

* **LinkedIn:** [linkedin.com/in/david-barcellos-cardoso](https://www.google.com/search?q=https://linkedin.com/in/david-barcellos-cardoso/)
* **GitHub:** [github.com/DBCBR](https://www.google.com/search?q=https://github.com/DBCBR)
