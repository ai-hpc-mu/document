
---

# 🚀 Deploying Qwen 3.5 122B on Mahidol Cluster
Author: Snit Sanhlao , AI Assitant Gemini 
### High-Performance Coding & Chat via 4-bit AWQ Quantization

This guide provides the configuration and setup for **Qwen 3.5**, optimized for resource-constrained GPU clusters. By utilizing **AWQ 4-bit quantization** and a **Mixture of Experts (MoE)** architecture, we achieve high-tier reasoning capabilities while significantly reducing VRAM footprint and token costs.

---

## 📊 Model Specifications

| Feature | Detail |
| --- | --- |
| **Model ID** | `cyankiwi/Qwen3.5-122B-A10B-AWQ-4bit` |
| **Architecture** | Mixture of Experts (MoE) |
| **Active Params** | ~10B (Efficiency of a 10B model, knowledge of a 122B) |
| **Quantization** | 4-bit AWQ (Activation-aware Weight Quantization) |
| **Context Window** | 32,768 Tokens (Optimized to 16,384 for stability) |
| **vLLM Engine** | V1 (Experimental Asynchronous Engine) |
| **API Endpoint** | `https://aicenter.mahidol.ac.th/vllm/v1` |

---

## 💻 IDE Integration (VS Code)

### Continue.dev Configuration

To use Qwen 3.5 as your coding assistant, update your `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Qwen 3.5 (Mahidol AI)",
      "provider": "openai",
      "model": "cyankiwi/Qwen3.5-122B-A10B-AWQ-4bit",
      "apiKey": "sk-xxxx",
      "apiBase": "https://aicenter.mahidol.ac.th/vllm/v1"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Qwen 3.5 Autocomplete",
    "provider": "openai",
    "model": "cyankiwi/Qwen3.5-122B-A10B-AWQ-4bit",
    "apiBase": "https://aicenter.mahidol.ac.th/vllm/v1"
  }
}

```

---

## 🌐 Open WebUI Deployment

The easiest way to interact with the model is via Open WebUI. Run the following Docker command to connect to the cluster:

```bash
docker run -d -p 3000:8080 \
  --name open-webui \
  --restart always \
  -e WEBUI_AUTH=False \
  -e OPENAI_API_BASE_URL=https://aicenter.mahidol.ac.th/vllm/v1 \
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
curl https://aicenter.mahidol.ac.th/vllm/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxxx" \
  -d '{
    "model": "cyankiwi/Qwen3.5-122B-A10B-AWQ-4bit",
    "messages": [{"role": "user", "content": "Explain the benefit of MoE architecture."}],
    "temperature": 0.7
  }'

```

---

## 🛠 Troubleshooting & Maintenance

| Symptom | Action |
| --- | --- |
| **Tokenizer Error** | Ensure vLLM is upgraded to support `TokenizersBackend` (transformers v5.0+). |
| **CUDA Out of Memory** | Lower `gpu-memory-utilization` to `0.80` or reduce `max-model-len`. |
| **504 Gateway Timeout** | The model is large; increase your client-side timeout (e.g., NGINX proxy-read-timeout). |
| **401 Unauthorized** | Verify your `sk-xxxx` API key is passed in the Authorization header. |

### Container Management

```bash
# View real-time logs
docker logs -f open-webui

# Stop and Clean up
docker stop open-webui && docker rm open-webui

```

---

## 📝 Usage Notes

* **Efficiency:** The `A10B` suffix indicates that only ~10B parameters are activated per token, making this much faster than a standard 122B dense model.
* **Architecture:** Uses the `Qwen3_5MoeForConditionalGeneration` architecture, optimized via FlashInfer.
* **Privacy:** All data remains within the Mahidol University infrastructure.
* **Security:** **Never** commit your actual `apiKey` to a public GitHub repository.

---

*Last Updated: 2026-03-05*

---
