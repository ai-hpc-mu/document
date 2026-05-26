# OpenClaw — Local Agentic AI Framework

### For Mahidol University AI Center — Researchers, Students & Staff

> **Reference:** `aicenter.mahidol.ac.th/qwen3-6-27b`

**Authors:** Snit Sanghlao, OpenClaw, Qwen, OpenCode

---

## Executive Summary

AI is shifting from chatbots to agents — from "tell me" to "I'll do it for you."

Anthropic recently closed off their community integrations (Claude Code CLI, cooperative agent frameworks), pulling powerful agentic capabilities behind closed doors. This leaves a critical gap for research and educational institutions that need **transparent, controllable, deployable** AI agents — especially for sensitive Thai language, local data, and compliance.

**OpenClaw is the open-source answer.** It is a full agentic AI framework that runs entirely locally — on your own servers, your own hardware, your own network. It pairs with open models like **Qwen3.6-27B** (27B parameters) to create a powerful, private, and persistent AI agent experience.

### Why This Matters Now

| | Anthropic Claude (Closed) | **OpenClaw × Qwen3.6-27B (Open & Local)** |
|---|---|---|
| **Data Privacy** | Cloud-only → your research leaves your campus | Runs locally → data never leaves your infrastructure |
| **Language Support** | Limited Thai/SE Asian language accuracy | Use Thai-language models (Qwen excels at multilingual) |
| **Customization** | Fixed rules, no modification | Full personality, workflow, and policy control |
| **Cost** | Ongoing subscription API fees | One-time compute — free after hardware |
| **Community** | Withdrawing from open ecosystem | Active open-source, SKill marketplace (ClawHub) |
| **Multi-Channel** | Single interface | Telegram, Discord, WhatsApp, WebChat, Slack, Signal |
| **Persistent Memory** | Stateless conversations | Long-term memory across sessions (your knowledge base) |
| **Agent Scheduling** | Task-specific | Built-in cron, heartbeats, proactive monitoring |

### Benefits — Now

1. **Research Acceleration** — Draft papers, analyze data, manage literature reviews, generate code
2. **Student Support** — 24/7 tutoring, research guidance, literature summaries
3. **Admin Efficiency** — Schedule management, email triage, knowledge base queries
4. **Thesis/Dissertation Help** — LaTeX writing, reference management, code debugging
5. **Data Analysis** — Run Python, shell commands, process files locally
6. **Device Integration** — Control servers, cameras, sensors paired as nodes

### Benefits — Future (Mahidol AI Center Vision)

1. **Institutional Knowledge Base** — Training the agent on internal research, policies, and procedures becomes your living reference system
2. **Multi-Agent Workflows** — Researchers spawn sub-agents to parallelize labs, code review, and experiments
3. **Custom Skills Marketplace** — Build and share skills tailored to Thai research domains (agriculture, medicine, marine science, NLP for Thai)
4. **Local-First AI Governance** — Full audit trail, no vendor lock-in, no data leakage risk
5. **Community Collaboration** — Share skills across Thai universities; contribute to the global open-agent ecosystem
6. **Cost-Scaling** — As Qwen and other open models improve, you benefit instantly with zero licensing changes

---

## User Guide — Setting Up OpenClaw with Qwen3.6-27B

### What You Need

- A Linux server (Ubuntu 22.04+, or similar)
- Node.js 20+ (or use nvm)
- GPU with ≥16GB VRAM for Qwen3.6-27B (A100/RTX 4090/RTX 3090) — or run CPU-only for lighter use
- Any LLM serving backend (vLLM, Ollama, LM Studio, or local OpenAI-compatible endpoint)

> For `qwen3-6-27b` on your server, ensure it's accessible at an OpenAI-compatible endpoint like:
> ```
> http://localhost:8000/v1
> ```

---

### Step 1 — Install OpenClaw

```bash
# Install via npm (requires Node.js 20+)
npm install -g openclaw

# Verify installation
openclaw --version
```

### Step 2 — Initialize Your Workspace

```bash
# This creates your workspace and config
openclaw init
```

This creates `~/.openclaw/` with:
- `config.yaml` — your main configuration
- `workspace/` — where your agent's files, memory, and projects live

### Step 3 — Configure the Model (Qwen3.6-27B)

> **Tip:** Use Mahidol AICenter endpoint: `https://aicenter.mahidol.ac.th/qwen3-6-27b/v1`

Edit `~/.openclaw/config.yaml`:

```yaml
model:
  provider: vllm                    # or ollama, lm-studio, anything OpenAI-compatible
  modelId: "Qwen/Qwen3.6-27B"
  apiBaseUrl: "http://localhost:8000/v1"
  apiKey: "none"                    # omit or set if your backend requires auth
  maxTokens: 8192                 # Max output tokens (8K - balanced for remote)
  contextWindow: 262144           # Context window (256K)

# Optional: if using Ollama instead
# model:
#   provider: ollama
#   modelId: "qwen3.6:27b"
```

#### maxTokens Recommendation

| maxTokens | Use Case | Latency |
|---|---|---|
| **4K** | Quick chat, simple tasks | Fastest |
| **8K** | Balanced — recommended for remote endpoints | Moderate |
| **16K** | Complex reasoning, longer outputs | Slower |
| **32K+** | Full papers, extensive code — local GPU only | Slowest |

> **For AICenter remote endpoint:** Use `maxTokens: 8192` (8K) for best balance of response length and speed.

### Step 4 — Start the Gateway

```bash
# Start the agent daemon
openclaw gateway start

# Check status
openclaw gateway status
```

The gateway listens on your server and exposes a web interface (webchat) plus messaging channels.

### Step 5 — Connect via Webchat (Quick Start)

By default, OpenClaw provides a web chat interface at:

```
http://your-server:3000
```

Visit it in your browser — that's your agent ready to go.

### Step 6 — Optional: Connect Messaging Channels

```yaml
# Add to config.yaml for Telegram
plugins:
  entries:
    telegram:
      token: "YOUR_BOT_TOKEN"
      name: "telegram"

# Add to config.yaml for Discord
  entries:
    discord:
      token: "YOUR_BOT_TOKEN"
      name: "discord"
```

Then restart:

```bash
openclaw gateway restart
```

---

## Connecting Qwen3.6-27B (Full Method)

### Option A — vLLM (Recommended for GPU)

```bash
# Install vLLM
pip install vllm

# Serve Qwen3.6-27B with GPU (256K context)
vllm serve Qwen/Qwen3.6-27B \
  --max-model-len 262144 \
  --tensor-parallel-size 1 \
  --port 8000
```

Your OpenClaw config:
```yaml
model:
  provider: vllm
  modelId: "Qwen/Qwen3.6-27B"
  apiBaseUrl: "http://localhost:8000/v1"
  maxTokens: 8192         # Max output tokens (8K - balanced for remote)
  contextWindow: 262144   # Context window (256K)
```

### Option B — Ollama (Easier Setup)

```bash
# Install Ollama (from https://ollama.com)
curl -fsSL https://ollama.com/install.sh | sh

# Pull Qwen
ollama pull qwen3.6:27b

# Verify it runs
ollama run qwen3.6:27b "hello"
```

Your OpenClaw config:
```yaml
model:
  provider: ollama
  modelId: "qwen3.6:27b"
```

### Option C — CPU Only (No GPU Required)

```bash
# Slow but works with Ollama + larger context
ollama pull qwen3.6:27b
```

---

## Customizing Your Agent

### Give It a Personality

Edit `workspace/SOUL.md`:

```markdown
# SOUL.md - Who You Are

## Core Truths
- Be helpful and resourceful
- Think in Thai context when user writes in Thai
- Be concise — not verbose
```

### Set Your Rules

Edit `workspace/AGENTS.md`:

```markdown
## Rules
- Never share research data externally
- Always ask before sending messages
- Use Thai language by default for local staff
```

### Set Long-Term Memory

Edit `workspace/MEMORY.md`:

```markdown
# OpenClaw Memory

*Key decisions, context, and knowledge base.*

## Notes
- [Date] Setup complete with Qwen3.6-27B on server X
- Active research areas: NLP, Computer Vision, Healthcare AI
```

### Memory Directory

Create a daily log folder:

```bash
mkdir -p /home/snit/.openclaw/workspace/memory
```

---

## What Can Your OpenClaw Agent Do? (Quick Reference)

| Category | Capability | Example |
|---|---|---|
| 📝 **Writing** | Papers, reports, LaTeX | "Draft a methods section for my ML paper" |
| 💻 **Coding** | Python, shell, any language | "Write a data preprocessing script" |
| 📚 **Research** | Literature search, summaries | "Summarize transformer papers from 2023" |
| 📅 **Scheduling** | Cron, reminders, heartbeat | "Remind me about the thesis deadline" |
| 🌐 **Web** | Browser control, fetch | "Check the latest arXiv papers on X" |
| 🗂️ **Files** | Read, edit, organize | "Reorganize my project folders" |
| 💬 **Messaging** | Multi-channel communication | "Send this summary to the department channel" |
| 📊 **Data** | Run analysis, visualize | "Process these CSV files and show summaries" |
| 🔐 **Memory** | Persistent across sessions | "Remember that server has 200TB storage" |
| 🤖 **Agents** | Spawn sub-agents for parallel work | "Research A and B in parallel" |

---

## Security Hardening — User Level

### Gateway Access Control

```bash
# Bind to localhost only (recommended for single-user)
openclaw config set gateway.bind loopback

# Or bind to LAN for local network access
openclaw config set gateway.bind lan
```

### Token Authentication

```bash
# Generate a new gateway token
openclaw devices pair --name "your-device"

# View current token
openclaw config get gateway.auth.token
```

### Rate Limiting

```bash
# Set rate limits in config
openclaw config set gateway.rateLimit.enabled true
openclaw config set gateway.rateLimit.maxRequests 100
openclaw config set gateway.rateLimit.windowMs 60000
```

### File System Permissions

```bash
# Secure workspace directory
chmod 700 ~/.openclaw/workspace
chmod 600 ~/.openclaw/openclaw.json
```

### Network Firewall (Linux)

```bash
# Allow only local access
sudo ufw allow 18789/tcp from 127.0.0.1
sudo ufw enable
```

### Environment Variables Security

```bash
# Never store API keys in config files; use environment variables
# In ~/.bashrc or ~/.profile:
export OPENCLAW_API_KEY="your-key-here"
```

### Disable Unused Channels

```yaml
# In config — disable channels you don't use
plugins:
  entries:
    telegram:
      enabled: false
    discord:
      enabled: false
```

### Regular Updates

```bash
# Keep OpenClaw updated
openclaw update check
openclaw update install
```

---

## Troubleshooting

### Agent won't start
```bash
openclaw gateway status   # check status
openclaw gateway restart  # restart
```

### Model connection errors
- Verify your model server is running and accessible
- Check `apiBaseUrl` points to the correct endpoint
- Test with: `curl http://localhost:8000/v1/models`

### Memory not persisting
- Ensure `workspace/` exists
- Check file permissions: `chmod 755 workspace/`

---

## Getting Help

- **Docs:** https://docs.openclaw.ai
- **Source:** https://github.com/openclaw/openclaw
- **Community:** https://discord.com/invite/clawd
- **Skills Marketplace:** https://clawhub.ai

---

*Built for institutions that refuse to compromise on privacy, control, and innovation.*

**Mahidol University AI Center** × **OpenClaw** × **Qwen3.6-27B**
