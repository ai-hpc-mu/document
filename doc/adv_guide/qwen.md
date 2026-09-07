# 🚀 Using Qwen on the Mahidol Cluster

**Author**: Snit Sanghlao, AI Assistant Gemini

### High-Performance Coding & Chat via the AI Center Qwen endpoint

This guide provides the configuration and setup for the **Qwen** large language model
served by the Mahidol AI Center. It is aimed at coding assistants (Continue.dev, agent
frameworks) and general chat via an OpenAI-compatible API.

---

## 📌 Stable Endpoint (read this first)

All examples target a **version-independent alias**:

| Setting | Value |
| --- | --- |
| **API Endpoint** | `https://aicenter.mahidol.ac.th/qwen/v1` |
| **Model ID** | `qwen` |
| **API style** | OpenAI-compatible (`/chat/completions`, `/completions`, `/models`) |

The `/qwen/v1` route is a **stable alias maintained by the AI Center**. It always points
to the current production Qwen deployment. When the model is upgraded, the alias is
repointed on the server side and **your configuration does not change** — the endpoint
URL and the model ID `qwen` stay the same.

> [!NOTE]
> **For the AI Center administrator:** the alias requires an NGINX route
> `/qwen/v1/ → <internal vLLM service>` and the vLLM server started with
> `--served-model-name qwen`. Serving-side details (hardware, parallelism,
> memory settings, node placement) are intentionally omitted from this guide.

### Check what is currently deployed

```bash
curl -sk https://aicenter.mahidol.ac.th/qwen/v1/models
```

The response reports the upstream checkpoint (`root`) and the maximum context length
(`max_model_len`) of whatever version is live. At the time of writing this resolves to
**Qwen3.8-27B** with a **256K** (262 144-token) context window.

---

## 💻 IDE Integration (VS Code)

### Continue.dev Configuration

To use Qwen as your coding assistant, update your `~/.continue/config.yaml`:

```yaml
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: Qwen
    provider: openai
    model: qwen
    apiBase: https://aicenter.mahidol.ac.th/qwen/v1
    systemMessage: "You are a helpful assistant."
    apiKey: "sk-xxxx"
    contextLength: 262144   # 256K context; lower it if your client is slow
    maxTokens: 4096         # Leave room for the model to respond
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

---

## 🌐 Open WebUI Deployment

The easiest way to interact with the model is via Open WebUI. Run the following Docker command to connect to the cluster:

```bash
docker run -d -p 3000:8080 \
  --name open-webui \
  --restart always \
  -e WEBUI_AUTH=False \
  -e OPENAI_API_BASE_URL=https://aicenter.mahidol.ac.th/qwen/v1 \
  -e OPENAI_API_KEY=sk-xxxx \
  -v open-webui:/app/backend/data \
  ghcr.io/open-webui/open-webui:main

```

> [!TIP]
> Use the `-d` (detached) flag instead of `-it` to keep the UI running in the background after you close your terminal.

---

## 🧪 Verification & Testing

### Connectivity Test (cURL)

Run this in your terminal to verify the endpoint is reachable and the model is loaded:

```bash
curl https://aicenter.mahidol.ac.th/qwen/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxxx" \
  -d '{
    "model": "qwen",
    "messages": [{"role": "user", "content": "Say hello in one sentence."}],
    "temperature": 0.7
  }'

```

---

## 🛠 Troubleshooting & Maintenance

| Symptom | Action |
| --- | --- |
| **404 / model not found** | Confirm `model` is set to `qwen`; run `curl .../qwen/v1/models` to see the served IDs. |
| **CUDA Out of Memory (self-hosted)** | Lower `gpu-memory-utilization` or reduce `max-model-len` on your own server. |
| **504 Gateway Timeout** | The model is large; increase your client-side timeout (e.g., NGINX `proxy-read-timeout`). |
| **401 Unauthorized** | Verify your `sk-xxxx` API key is passed in the `Authorization` header. |

### Container Management

```bash
# View real-time logs
docker logs -f open-webui

# Stop and Clean up
docker stop open-webui && docker rm open-webui

```

---

## 📝 Usage Notes

* **Version independence:** Always target `https://aicenter.mahidol.ac.th/qwen/v1` with model `qwen`. Do not hard-code a version number — when the deployment is upgraded the alias moves and your config keeps working.
* **Privacy:** All data remains within the Mahidol University infrastructure.
* **Security:** **Never** commit your actual `apiKey` to a public GitHub repository.

---

*Last Updated: 2026-09-07*
