# Architecture

Request path in short form:

Customer or client hits the API. The API may retrieve private policy context, call the LLM, and/or accept a proposed tool call. Validation and execution live in application code. The orders package owns database work. The model never gets a DB connection or payment credentials.

Layers grow in this order: orders, llm, rag, evals, tools, observability, then cloud deploy.

Update this file when the real request flow changes.
