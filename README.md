# Order Support Agent

This repo is one product: a backend that helps customers with delivery orders. It answers from private policy docs and can trigger safe order actions. The model never talks to the database or payments. It proposes an action. The app validates it. An order service runs it.

This is the portfolio piece for moving into AI engineering. Everything below is built in the same codebase over about 90 days.

## What it becomes

A customer asks something like "what is the refund if I cancel" or "cancel my order". The API may retrieve restaurant policies, cancellation rules, delivery FAQs, and current offers, then return a grounded answer. When an action is needed, tools such as getOrderStatus and cancelOrder go through validation first.

By the end you should be able to show reliability under failure, a RAG pipeline with a fixed question set, an eval harness that catches regressions, safe tool calling, observability (where, why, cost, user impact), and a cloud deploy with load and failure checks.

## Repo layout

```
app/
  api/             HTTP routes
  core/            config, auth, logging
  orders/          create, status, cancel, refund (no LLM)
  llm/             prompts, client, structured output
  rag/             ingest, chunk, embed, retrieve
  tools/           propose, validate, execute
  evals/           golden questions and harness
  observability/   metrics, traces, cost
docs/              architecture and decisions
policies/          source docs for retrieval
scripts/           seed, evals, load tests
tests/
```

Folders fill in as phases unlock. Do not invent services early. One FastAPI process plus Postgres is enough for a long time. A vector store comes with RAG.

## Before the 90 days

Lock in FastAPI, Pydantic, pytest, async, and Postgres on a small API first. Then build the real order service (REST, indexes, concurrency, transactions). That order service stays. Later the model only proposes calls into it.

## 90 day plan

**Days 1 to 15. LLM fundamentals**

Client hits the backend. Backend calls the LLM with prompts, structured JSON, system instructions, context window, temperature, and token usage. Return a structured response.

**Days 16 to 30. Backend reliability**

Add auth, timeouts, retries, rate limits, logs, and cost tracking. Happy path is not enough. Failures must behave predictably.

Checkpoint at day 30: one AI app that still works when the provider misbehaves.

**Days 31 to 45. RAG**

Connect the model to private domain knowledge for this delivery business. Implement documents, ingestion, chunking, embeddings, vector search, retrieval, context injection, then a grounded answer.

Build 20 to 30 real user style questions (refund after cancel, late delivery refund, weekend offers). After each change, check whether answers actually improved.

Checkpoint at day 45: RAG pipeline plus a representative test set.

**Days 46 to 55. Evals**

Turn those questions into an engineering loop. For each question, define what a good answer looks like. Compare versions when you change the prompt, the model, or retrieval. Detect improvement versus noise.

Checkpoint at day 55: a basic eval harness.

**Days 56 to 65. Tool calling**

Move from answers only to safe business actions. Model proposes. App validates. Order service executes. No direct model access to DB or payments.

Checkpoint at day 65: an AI triggered, deterministic business flow.

**Days 66 to 75. Observability**

Track latency, tokens, cost per request, error rate, retries, traces. Then break things on purpose: LLM timeout, provider error, slow retrieval, tool failure, retry storm. For each case answer where it failed, why, what it cost, and what the user felt.

Checkpoint at day 75: you can observe and debug, not only build.

**Days 76 to 85. Deploy and harden**

Move off localhost. Prove secrets management, rate limits, retries, recovery, latency, and cost still hold. Load test. Know how the system behaves when the LLM is down, the vector path is slow, or a tool fails.

**Days 86 to 90. Ship**

Ship the hardened system. Tag a release. Make the README and architecture notes match what actually runs.

## Timeline

1. Days 1 to 15, LLM fundamentals: client to API to LLM to structured response.
2. Days 16 to 30, reliability: auth, timeouts, retries, rate limits, logs, cost.
3. Days 31 to 45, RAG: retrieval over private docs plus 20 to 30 questions.
4. Days 46 to 55, evals: harness that flags better versus just different.
5. Days 56 to 65, tools: propose, validate, execute.
6. Days 66 to 75, observability: where, why, cost, impact under injected failures.
7. Days 76 to 85, deploy: cloud, secrets, load, failure behavior.
8. Days 86 to 90, ship: tagged release that matches the docs.

## Safety rule

The model does not get the database. The model does not get payment systems. It can suggest getOrderStatus or cancelOrder. Application code decides if that is allowed. The orders package does the work.

## Local setup

Python 3.11+ recommended. Create a virtualenv, install from `pyproject.toml`, copy `.env.example` to `.env`, and fill in DB credentials there. Never commit `.env`.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
copy .env.example .env   # Windows
# cp .env.example .env   # Unix
# edit .env: POSTGRES_* and DATABASE_URL
docker compose up -d
uvicorn app.main:app --reload
```

`docker-compose.yml` reads passwords from `.env` only. Do not put real keys, tokens, or DB passwords in source, `.env.example`, or commit history.

## Resume angle

One system, not a pile of demos. In an interview you can walk through a wrong refund answer, a double-cancel race, a provider timeout, or a retrieval change that made evals worse — that is why every phase stays in this repo.
