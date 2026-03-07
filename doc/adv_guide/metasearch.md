# Metasearch for AI-Powered Organizations
### A Guide to SearXNG Federated Search on the Cluster

**Authors:** Snit Sanghlao, Claude Sonnet 4.6 (Anthropic)
**Date:** March 2026
**Instance:** `https://aicenter.mahidol.ac.th/metasearch/`

---

## What is Metasearch?

A **metasearch engine** (also called a federated search engine) queries multiple search engines simultaneously, aggregates and deduplicates the results, and returns a unified ranked list — without storing user data or tracking queries.

**SearXNG** is an open-source, self-hosted metasearch engine. A single query to SearXNG can simultaneously retrieve results from:

| Category | Sources |
|----------|---------|
| General Web | DuckDuckGo, Brave, Bing |
| Academic | Google Scholar, arXiv, PubMed, Semantic Scholar, Crossref |
| Reference | Wikipedia |
| Code | GitHub, StackOverflow |

---

## Why Metasearch Matters for Organizations

| Concern | Problem with Public Search Engines | Metasearch Solution |
|---------|------------------------------------|---------------------|
| **Privacy** | Google/Bing log every query and link it to user identity | No tracking, no logs, self-hosted |
| **Data Leakage** | Sensitive queries are sent to external commercial companies | All queries remain within organizational infrastructure |
| **Compliance** | PDPA / GDPR risk when employees search sensitive topics | On-premise, auditable, policy-controlled |
| **Coverage** | Single engine = single index = blind spots in results | Multiple sources = broader, more complete results |
| **Cost** | Enterprise search APIs charge per query at scale | Free, self-hosted, unlimited queries |
| **Control** | Cannot restrict or customize engines used | Full control over enabled engines, categories, and filters |

---

## Why Metasearch is Critical for AI Agentic Systems

AI agents need **reliable, real-time, broad information access** to reason and act effectively. Metasearch is a foundational infrastructure component for agentic AI.

### 1. Grounding — Reducing Hallucination
Language models have a knowledge cutoff. Agents that can search retrieve **current, factual information** and use it as context, grounding answers in reality rather than memorized training data.

### 2. Clean API for Tool Use
AI agents call APIs, not browsers. SearXNG exposes a standard **JSON REST API**:
```
GET /search?q={query}&format=json
```
Any agent, LLM framework, or RAG pipeline can call this directly — no scraping, no browser automation required.

### 3. Multi-Source in One Request
A single SearXNG query returns results from PubMed, arXiv, Semantic Scholar, and news sources **simultaneously** — without requiring separate API keys or integrations for each source.

### 4. Private Agentic Workflows
When an AI agent performs sensitive tasks (patient data analysis, competitor research, legal document review), those queries must not leak to external companies. A private metasearch instance ensures **all agent activity stays internal**.

### 5. RAG Pipeline Integration
In Retrieval-Augmented Generation (RAG), SearXNG acts as the **live web retrieval layer**, complementing internal vector databases with fresh knowledge:

```
User Query
    │
    ▼
  Agent
    │
    ├──► SearXNG (live web)      ──► Top N results ──┐
    │                                                  ├──► LLM Context ──► Answer
    └──► Vector DB (internal docs) ──► Top K chunks ──┘
```

### 6. Compatible with Major AI Frameworks

| Framework / Tool | Integration |
|-----------------|-------------|
| OpenWebUI | Built-in web search toggle |
| Continue (VS Code) | `@search` context provider |
| LangChain | SearxNG search tool |
| LlamaIndex | Web retrieval node |
| AutoGen / CrewAI | Custom agent tool via REST API |
| Any custom agent | Direct HTTP JSON API |

---

## Using SearXNG on This Cluster

### Option 1: OpenWebUI

**Setup (Admin only)**

Go to: `Admin Panel → Settings → Web Search`
- Web Search Engine: `searxng`
- SearXNG Query URL: `https://aicenter.mahidol.ac.th/metasearch/search?q=<query>`

**How to Use (All users)**

1. Open a new chat in OpenWebUI
2. Click the **globe icon** at the bottom of the chat input bar
3. The icon highlights when web search is active
4. Type your question and send — the model will search and answer using live results

> Web search is toggled per message. You can enable or disable it for each individual message.

---

### Option 2: Continue VS Code Extension

Continue uses SearXNG as a **context provider**. When you type `@web`, Continue fetches results from SearXNG and injects them into the model's prompt before sending — the model itself does not browse the web.

#### Step 1: Configure Continue

**PC (Local Windows)**

Config file: `C:\Users\<your-username>\.continue\config.yaml`

```yaml
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: Qwen3.5
    provider: openai
    model: cyankiwi/Qwen3.5-122B-A10B-AWQ-4bit
    apiBase: https://aicenter.mahidol.ac.th/vllm/v1
    apiKey: "sk-xxxx"
    requestOptions:
      extraBodyProperties:
        chat_template_kwargs:
          enable_thinking: false
context:
  - provider: web
    params:
      engine: "searxng"
      query: ""
      searxngBaseUrl: https://aicenter.mahidol.ac.th/metasearch/
      n: 5
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: problems
  - provider: folder
  - provider: codebase
```

**Remote SSH (Linux Cluster)**

Connect to the cluster via VS Code Remote SSH, then run:

```bash
mkdir -p ~/.continue
nano ~/.continue/config.yaml
```

Paste the same config above, save (`Ctrl+O` → Enter → `Ctrl+X`).

#### Step 2: Reload VS Code

Press `Ctrl+Shift+P` → `Developer: Reload Window`

#### Step 3: Use @web in Chat

1. Open the Continue chat panel
2. Type `@` — a dropdown appears
3. Select **web** from the list
4. Type your query followed by your question:

```
@web transformer architecture survey 2024
Summarize the key improvements in recent transformer models.
```

5. Press **Enter** — Continue fetches results from SearXNG and the model answers using those results as context

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `@web` not in dropdown after `@` | Reload VS Code: `Ctrl+Shift+P` → `Developer: Reload Window` |
| Dropdown appears but no `web` option | Check `config.yaml` is valid YAML — use a YAML validator |
| Globe icon missing in OpenWebUI | Ask admin to enable Web Search in Admin Panel |
| SearXNG not reachable | Open `https://aicenter.mahidol.ac.th/metasearch/` in your browser |
| Model says it cannot search | Use `@web` — the model has no built-in search; Continue injects results as context |
| Remote SSH config not loading | Ensure config is at `~/.continue/config.yaml` on the **remote** server, not local |

**Verify SearXNG API is working:**

```bash
curl "https://aicenter.mahidol.ac.th/metasearch/search?q=test&format=json"
```

Expected: a JSON object with a `results` array containing search hits.

---

## Summary

> Metasearch is the **search infrastructure layer** for AI — it gives agents and users access to the open web privately, broadly, and without per-query cost. For organizations handling sensitive data, a self-hosted metasearch instance is essential infrastructure for any AI workload that requires real-world knowledge.

---

## References

1. SearXNG Documentation. *SearXNG: A privacy-respecting, hackable metasearch engine.* https://docs.searxng.org/
2. Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* arXiv:2005.11401. https://arxiv.org/abs/2005.11401
3. Continue. *Context Providers — Search.* https://docs.continue.dev/customize/context-providers
4. OpenWebUI. *Web Search Integration.* https://docs.openwebui.com/features/web_search
5. Anthropic. (2025). *Claude Sonnet 4.6 Model Card.* https://www.anthropic.com/

---

*This document was co-authored by Snit Sanghlao and Claude Sonnet 4.6 (Anthropic), March 2026.*
