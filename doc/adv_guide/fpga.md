# Gowin FPGA AI Workflow — User Guide

### Mahidol University AI Center · Design House R&D Laboratory

**System:** OpenClaw × Qwen3.6-27B × Gowin MCP × Obsidian × Slack  
**Hardware:** Sipeed Tang Mega 138K · GW5AST-138B/C BGA484  
**Authors:** Snit Sanghlao · Anthropic Claude · OpenClaw · Mahidol AI Center

---

## Executive Summary

### What This System Does

The Mahidol AI Center Design House has deployed an AI-assisted FPGA development workflow that connects a locally-hosted AI agent directly into the hardware design pipeline. Engineers can issue natural-language commands via Slack or a web interface to synthesize, place-and-route, and flash Gowin FPGA bitstreams — without manually running toolchain commands.

All compute, models, and data remain on-premise. No research IP leaves the laboratory network.

### Business Value

| Dimension | Before | After |
|---|---|---|
| **Synthesis trigger** | Engineer opens IDE, configures run, waits | Single message in Slack — AI handles the rest |
| **Knowledge retention** | Scattered notes, terminal history | Persistent Obsidian vault indexed by the AI |
| **Toolchain expertise** | Each researcher learns CLI from scratch | AI agent guides with exact commands and warnings |
| **Debugging** | Manual log reading | AI parses build logs, flags errors in plain language |
| **Remote operation** | Must be at workstation | Command from any device via Slack |
| **Data sovereignty** | N/A — closed cloud tools not used | 100% on-premise; no cloud vendor dependency |

### Key Capabilities — Now Available

1. **Conversational FPGA builds** — "Build my LDPC project and flash to the board" triggers synthesis → P&R → programming automatically
2. **Intelligent error reporting** — Failed builds produce human-readable summaries with specific fix guidance
3. **Board setup guidance** — Agent provides DBG_BOOT, DIP switch, and udev instructions on demand
4. **Design knowledge base** — Obsidian vault stores project history, design decisions, and research notes; the AI searches it in real time
5. **Slack integration** — Full command access from `#all-openclaw-ws`; agent participates in team discussion
6. **Persistent memory** — Agent remembers project context, server configs, and past decisions across sessions

### Who Should Read This Guide

- **Lab managers / PI** — Executive Summary (this section)
- **FPGA design engineers** — Quick Start, MCP Tools Reference, Workflow Examples
- **System administrators** — Installation, Security, Troubleshooting

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAHIDOL AI CENTER — ON-PREMISE               │
│                                                                 │
│  ┌───────────────┐   ┌─────────────────────────────────────┐   │
│  │ Slack Channel │   │         OpenClaw Gateway             │   │
│  │ #all-openclaw │──▶│   (Node.js daemon, port 18789)       │   │
│  │      -ws      │◀──│   Model: Qwen3.6-27B (256K context)  │   │
│  └───────────────┘   │   Endpoint: aicenter.mahidol.ac.th  │   │
│                      └─────────────┬───────────────────────┘   │
│  ┌───────────────┐                 │                           │
│  │ Web Chat UI   │                 │ MCP Protocol              │
│  │ localhost:    │◀────────────────┤                           │
│  │    18789      │                 │                           │
│  └───────────────┘        ┌────────▼────────┐                  │
│                           │   MCP Servers   │                  │
│                      ┌────┴──┐         ┌───┴──────────────┐   │
│                      │Obsidian│         │ gowin-workflow   │   │
│                      │ Vault  │         │  mcp_server.py   │   │
│                      │  MCP   │         └───────┬──────────┘   │
│                      └────────┘                 │              │
│  ┌─────────────────────────────────┐    ┌───────▼──────────┐   │
│  │     Obsidian Second Brain       │    │  Gowin Toolchain  │   │
│  │  openclaw-second-brain/ vault   │    │  ├─ gw_sh (IDE)   │   │
│  │  ├─ MAI/guide/                  │    │  ├─ programmer_cli│   │
│  │  └─ Project notes & decisions   │    │  └─ openFPGALoader│   │
│  └─────────────────────────────────┘    └───────┬──────────┘   │
│                                        ┌────────▼──────────┐   │
│                                        │ Tang Mega 138K    │   │
│                                        │ GW5AST-138B BGA484│   │
│                                        │ USB DEBUG-USB2    │   │
│                                        └───────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Map

| Component | Role | Location |
|---|---|---|
| **OpenClaw** | AI agent daemon, gateway, memory | `~/.openclaw/` |
| **Qwen3.6-27B** | Local LLM (27B, 256K context) | `https://aicenter.mahidol.ac.th/qwen3-6-27b/v1` |
| **gowin-workflow MCP** | FPGA toolchain tools over MCP | `/media/snit/AiHPC/tools/vlsi/gowin/mcp_server.py` |
| **obsidian-vault MCP** | Second brain file access | `@modelcontextprotocol/server-filesystem` |
| **Obsidian vault** | Knowledge base, notes, memory | `/home/snit/ai/obsidian-noted/openclaw-second-brain/` |
| **Slack** | Team communication channel | `#all-openclaw-ws` |
| **Tang Mega 138K** | Target FPGA board | Physical hardware, USB JTAG |

---

## Technical Perspective

### MCP Architecture

OpenClaw exposes hardware tools to the AI agent via the **Model Context Protocol (MCP)** — a standardized JSON-RPC interface that lets a language model call structured tools with typed parameters and receive structured results. Two MCP servers are registered:

#### 1. `gowin-workflow` — FPGA Toolchain Server

**Path:** `/media/snit/AiHPC/tools/vlsi/gowin/mcp_server.py`  
**Runtime:** Python 3.11 venv at `/media/snit/AiHPC/tools/vlsi/gowin/.venv/`  
**Transport:** stdio (spawned by OpenClaw on demand)

The server wraps four toolchain binaries:

| Binary | Purpose |
|---|---|
| `gw_sh` | Gowin IDE headless TCL shell — synthesis + P&R |
| `programmer_cli` | Gowin official programmer — cable/device scan |
| `openFPGALoader` | Open-source JTAG programmer — flash + detect |
| `lsusb` / `bflb-mcu-tool` | USB detection + BL616 firmware update |

**Environment management:** The server injects `LM_LICENSE_FILE=YOUR_LICENSE_SERVER`, `QT_QPA_PLATFORM=offscreen`, and the Gowin IDE `LD_LIBRARY_PATH` for every headless toolchain call — no shell setup required from the user.

**JTAG guard:** `flash_bitstream` and `build` both call `_require_jtag_mode()` before touching the board. This runs `lsusb` and checks for `0403:6010` (FT2232 in JTAG mode). If missing, the tool returns step-by-step DBG_BOOT instructions rather than failing silently.

#### 2. `obsidian-vault` — Knowledge Base Server

**Command:** `npx -y @modelcontextprotocol/server-filesystem /home/snit/ai/obsidian-noted/openclaw-second-brain`  
**Transport:** stdio

Provides the agent with read/write access to the full Obsidian vault. The agent can search design notes, update project logs, and retrieve historical context mid-conversation.

### OpenClaw Configuration (`~/.openclaw/openclaw.json`)

```json
{
  "models": {
    "providers": {
      "vllm": {
        "baseUrl": "https://aicenter.mahidol.ac.th/qwen3-6-27b/v1",
        "models": [{ "id": "Qwen/Qwen3.6-27B", "maxTokens": 262144 }]
      },
      "ollama": {
        "baseUrl": "http://localhost:11434/v1",
        "models": [{ "id": "qwen3.6:27b", "maxTokens": 4096 }]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "vllm/Qwen/Qwen3.6-27B" },
      "contextTokens": 256000
    }
  }
}
```

The primary model is the remote Mahidol AICenter endpoint (256K context). The local Ollama instance serves as fallback when the remote is unreachable.

### Slack Integration

The agent connects to Slack via Socket Mode (no public webhook required):

- **Bot token:** `xoxb-...` — workspace API access
- **App token:** `xapp-...` — Socket Mode connection
- **Channel:** `#all-openclaw-ws` — interactive replies enabled
- **Policy:** `groupPolicy: open` — any channel member can invoke the agent

Messages sent to the channel are processed by the agent. The agent can reply, react with emoji, and trigger MCP tool calls in response to natural language.

---

## Quick Start

### Prerequisites

Before first use, verify these are in place:

```bash
# 1. Check OpenClaw is running
openclaw gateway status

# 2. Verify MCP servers registered
openclaw mcp show gowin-workflow
openclaw mcp show obsidian-vault

# 3. Check model endpoint is reachable
curl https://aicenter.mahidol.ac.th/qwen3-6-27b/v1/models

# 4. Check USB device permissions (if using FPGA)
lsusb | grep -E "1a86|0403"
```

### Start the Gateway

```bash
openclaw gateway start

# Verify
openclaw gateway status
# → Gateway running on http://localhost:18789
```

### Access Points

| Interface | URL / Channel |
|---|---|
| Web Chat | `http://localhost:18789` |
| Slack | `#all-openclaw-ws` |

---

## FPGA Hardware Setup

### Tang Mega 138K Board Overview

**Device:** GW5AST-138B/C · BGA484 · 138K LUT4  
**Debugger:** BL616 onboard (USB-C port labeled `DEBUG-USB2`)  
**Programming interface:** JTAG via FT2232 (activated via DBG_BOOT button or BL616 firmware update)

### DIP Switch Settings

Set all 5 DIP switches to **OFF** for normal JTAG programming:

| SW1 | SW2 | SW3 | SW4 | SW5 | Mode |
|-----|-----|-----|-----|-----|------|
| OFF | OFF | OFF | OFF | OFF | **JTAG programming — use this** |

### Activating JTAG Mode (Required Every Session)

The BL616 debugger defaults to CDC mode on power-up. To enable JTAG:

1. Set all DIP switches to **OFF**
2. Unplug the **DEBUG-USB2** USB-C cable
3. Hold the **DBG_BOOT** button (small button below the DEBUG-USB2 port on the **top** of the PCB)
4. Plug the cable back in while holding the button
5. Hold ~1 second, then release

**Verify JTAG mode is active:**
```bash
lsusb | grep 0403:6010
# Expected: Bus 00X Device 0XX: ID 0403:6010 Future Technology Devices International, Ltd FT2232C/D/H
```

> **One-time fix:** Flash the BL616 firmware once (see BL616 section) to make JTAG mode the permanent default — no button press needed again.

### USB Permissions (Run Once)

```bash
# BL616 / WCH
echo 'ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="fe0c", MODE:="666"' | \
    sudo tee /etc/udev/rules.d/51-gowin-bl616.rules

# FT2232 JTAG
echo 'ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", MODE:="666"' | \
    sudo tee /etc/udev/rules.d/51-gowin-ftdi.rules

# Gowin official rules
sudo cp /media/snit/AiHPC/projects/ldpc/aiChipDC/Programmer/bin/50-programmer_usb.rules \
    /etc/udev/rules.d/

sudo udevadm control --reload-rules && sudo udevadm trigger
```

Unplug and replug the USB cable after running.

---

## MCP Tools Reference

All tools are accessible by the AI agent. Engineers can also trigger them by describing the action in natural language via Slack or web chat.

### Device Detection

#### `check_usb_devices`
Lists Gowin-related USB devices (BL616, FT2232, WCH variants).
```
Ask: "Check what USB devices are connected"
```

#### `scan_cables`
Scans for programmer cables via `programmer_cli --scan-cables L`.
```
Ask: "Scan for programmer cables"
```

#### `scan_devices`
Scans for Gowin FPGA devices via `programmer_cli --scan`.
```
Ask: "Scan for FPGA devices"
```

#### `detect_fpga`
Detects FPGA via `openFPGALoader -b tangmega138k --detect`. Requires JTAG mode active.
```
Ask: "Detect the FPGA"
Expected: index 0 / GW5AST-138 / idcode 0x1081b
```

#### `get_device_info`
Runs both `scan_devices` and `check_usb_devices` in one call — good for a full status check.
```
Ask: "Give me full device info"
```

### Build Pipeline

#### `synthesize(project_path)`
Runs Gowin synthesis headlessly via `gw_sh`. Outputs go to `impl/gwsynthesis/` beside the project file.

```
Ask: "Synthesize /media/snit/AiHPC/projects/ldpc/mydesign/mydesign.gprj"
Timeout: 5 minutes
```

#### `implement(project_path)`
Runs place-and-route headlessly. Produces a `.fs` bitstream in `output/` beside the project file.

```
Ask: "Run P&R on my project"
Timeout: 10 minutes
Output: output/<top>.fs
```

#### `build(project_path, do_flash=True)`
Full pipeline: synthesis → P&R → flash to external SPI flash.

```
Ask: "Build and flash /path/to/project.gprj"
Timeout: 15 minutes total
Note: checks JTAG mode before starting — will abort with instructions if board not ready
```

`do_flash=False` builds only, no programming:
```
Ask: "Build without flashing"
```

### Programming

#### `flash_bitstream(fs_file, to_flash=True)`
Flashes a `.fs` bitstream file to the Tang Mega 138K via `openFPGALoader`.

| Parameter | Values | Effect |
|---|---|---|
| `to_flash=True` | Default | Writes to external SPI flash — **survives power cycle** |
| `to_flash=False` | SRAM only | Fast, lost on power cycle — good for testing |

```
Ask: "Flash /path/to/bitstream.fs to the board"
Ask: "Load bitstream to SRAM only for testing"
Timeout: 3 minutes
```

#### `list_bitstreams(directory)`
Lists all `.fs` files in a directory tree.
```
Ask: "List available bitstreams in my project folder"
```

### Setup & Maintenance

#### `get_dip_switch_config`
Returns the DIP switch guide for all board modes.
```
Ask: "What DIP switch settings do I need?"
```

#### `install_udev_rules`
Returns the exact commands to install USB udev rules.
```
Ask: "How do I fix USB access permissions?"
```

#### `update_bl616_firmware(firmware_path, port)`
Updates the BL616 onboard debugger firmware — makes JTAG mode permanent.

**Before running:**
1. Set all DIP switches OFF
2. Hold DBG_BOOT and plug DEBUG-USB2 cable
3. Verify `/dev/ttyACM0` is present

```
Ask: "Update the BL616 firmware"
Firmware: /tmp/bl616_NeoDock.bin
Port: /dev/ttyACM0
```

Download firmware if needed:
```bash
wget https://api.dl.sipeed.com/TANG/Debugger/onboard/BL616/2025030317/bl616_fpga_partner_NeoDock.bin \
    -O /tmp/bl616_NeoDock.bin
```

---

## Workflow Examples

### Example 1 — Daily Build and Flash

In Slack `#all-openclaw-ws`:

```
Engineer: Build and flash the LDPC project
Agent:    Checking JTAG mode... ✅ FT2232 detected.
          Running synthesis... [5 min]
          Running P&R... [8 min]
          Flashing to external SPI flash... [1 min]
          ✅ Build + flash succeeded.
          Bitstream: output/ldpc_top.fs
```

### Example 2 — Quick SRAM Test

```
Engineer: Flash the latest bitstream to SRAM for a quick test
Agent:    Listing bitstreams in /media/snit/AiHPC/projects/ldpc/...
          Found: output/ldpc_top.fs (2026-04-27 14:32)
          Loading to SRAM (not persistent)...
          ✅ SRAM load succeeded.
```

### Example 3 — Board Not Ready

```
Engineer: Detect FPGA
Agent:    ⚠️ Board not in JTAG mode (FT2232 not detected on USB).

          To activate JTAG mode:
            1. Unplug the DEBUG-USB2 cable
            2. Hold the DBG_BOOT button (below DEBUG-USB2, TOP of PCB)
            3. Plug back in while holding
            4. Release after ~1 second

          Then retry.
```

### Example 4 — Design Knowledge Query

```
Engineer: What was the last change we made to the LDPC encoder constraints?
Agent:    [searches Obsidian vault]
          From MAI/notes/ldpc-design-log.md (2026-04-15):
          "Updated timing constraint for encoder output to 250 MHz target.
           Previous was 200 MHz — required pipeline stage insertion in enc_out_reg."
```

### Example 5 — Full Setup from Scratch

```
Engineer: I just plugged in the board. What do I need to do?
Agent:    1. Check DIP switches → all OFF
          2. Activate JTAG mode (DBG_BOOT button sequence)
          3. Verify: lsusb | grep 0403:6010
          4. If USB access denied: run install_udev_rules commands

          Want me to check if the board is detected now?
```

---

## Obsidian Integration

### What the Agent Can Access

The `obsidian-vault` MCP server gives the agent full read/write access to:

```
/home/snit/ai/obsidian-noted/openclaw-second-brain/
├── MAI/
│   ├── guide/          ← This document lives here
│   └── ...
├── [project notes]
├── [design decisions]
└── [research logs]
```

### Practical Uses for FPGA R&D

1. **Design decision logging** — Ask the agent to record why a specific architecture choice was made
2. **Build history** — Log successful bitstreams, timing results, resource utilization
3. **Error knowledge base** — When a synthesis error is resolved, document the fix
4. **Cross-session memory** — Context from last week's session is available today

### Writing to the Vault via Agent

```
Engineer: Save a note that we changed the FIFO depth from 256 to 512 today
          to fix the backpressure issue

Agent:    [creates/updates MAI/notes/design-log-2026-04-27.md]
          Saved: "2026-04-27 — FIFO depth increased 256→512 to resolve
          encoder backpressure under max throughput."
```

---

## Slack Integration

### Channel: `#all-openclaw-ws`

The agent is live in this channel with `interactiveReplies` enabled. It:
- Responds when mentioned or directly addressed
- Reacts with emoji when appropriate (no unnecessary replies)
- Can trigger any MCP tool from a natural-language message
- Stays quiet during human-to-human discussion

### Invocation Examples

```
@openclaw build and flash my project at /media/.../mydesign.gprj
@openclaw what's the DIP switch config for JTAG?
@openclaw scan for USB devices
@openclaw check the Obsidian vault for notes on the LDPC timing closure
```

### Agent Behavior in Group Channels

Per the agent's workspace rules:
- Responds when directly asked or when it can add genuine value
- Does **not** respond to every message — participates like a human team member
- Uses single emoji reactions (👍, ✅) instead of text replies for acknowledgements
- Avoids dominating the conversation

---

## Gowin Toolchain Reference

### Paths (Current Installation)

| Tool | Path |
|---|---|
| `gw_sh` (headless IDE) | `/media/snit/AiHPC/projects/ldpc/aiChipDC/IDE/bin/gw_sh` |
| `programmer_cli` | `/media/snit/AiHPC/projects/ldpc/aiChipDC/Programmer/bin/programmer_cli` |
| `openFPGALoader` | `~/.local/bin/openFPGALoader` |
| IDE lib directory | `/media/snit/AiHPC/projects/ldpc/aiChipDC/IDE/lib` |

### License

```
LM_LICENSE_FILE=YOUR_LICENSE_SERVER
```

### Headless Build (Manual TCL)

```bash
export LM_LICENSE_FILE=YOUR_LICENSE_SERVER
export QT_QPA_PLATFORM=offscreen
export LD_LIBRARY_PATH=/media/snit/AiHPC/projects/ldpc/aiChipDC/IDE/lib:$LD_LIBRARY_PATH

cat > /tmp/build.tcl << 'EOF'
open_project /path/to/project.gprj
run syn
run pnr
exit
EOF

/media/snit/AiHPC/projects/ldpc/aiChipDC/IDE/bin/gw_sh /tmp/build.tcl
# Bitstream output: output/<top>.fs
```

### Programming Commands (Manual)

```bash
# Detect FPGA (JTAG mode required)
openFPGALoader -b tangmega138k --detect

# Flash to external SPI (persistent)
openFPGALoader -b tangmega138k -f /path/to/bitstream.fs

# Load to SRAM only (fast, volatile)
openFPGALoader -b tangmega138k /path/to/bitstream.fs

# Gowin programmer_cli scan
programmer_cli --scan
```

---

## Security & Operations

> Security protocols sourced from the Mahidol AI Center Obsidian vault:
> `MCP_CHECKLIST.md` · `Paths_Reference.md` · `Path-Verification-Log.md` ·
> `add Slack.md` · `add Obsidian.md` · `DNS.md` · `2026-04-27-Slack-OpenClaw-LLM-Fix.md`

---

### 1. Network Isolation

- OpenClaw gateway binds to **loopback only** (`gateway.bind: loopback`) — not reachable from LAN by default
- Slack connects via **Socket Mode** — no inbound port, no public URL, no firewall rule needed
- Model endpoint uses **HTTPS** to `aicenter.mahidol.ac.th` — encrypted in transit
- No external cloud APIs; all compute and data remain on Mahidol infrastructure

**Firewall (optional — restrict gateway port further):**
```bash
sudo ufw allow 18789/tcp from 127.0.0.1
sudo ufw enable
```

**Campus network note (from `DNS.md`):** The Mahidol campus network blocks outbound DNS to public resolvers (1.1.1.1, 8.8.8.8) — do not change system DNS away from `192.168.1.1`. If this machine is a Kubernetes master, DNS changes propagate to all pods. Use the router's upstream DNS settings instead of per-host overrides.

---

### 2. Authentication

#### Gateway Token
```bash
# Generate a new device token
openclaw devices pair --name "lab-workstation"

# View current token
openclaw config get gateway.auth.token
```

#### Slack Bot Token Scopes (Least Privilege)
From `add Slack.md` — grant only the minimum required scopes when creating the Slack App:

| Scope | Purpose |
|---|---|
| `app_mentions:read` | Detect @mentions |
| `chat:write` | Send messages |
| `im:history` | Read DMs |
| `im:read` | List DMs |
| `im:write` | Open DM channels |

No admin, file, or user-management scopes are needed or should be granted.

#### Slack Device Pairing (Security-First Protocol)
From `add Slack.md` — OpenClaw requires explicit approval before responding to any Slack account:

```bash
# 1. Find the bot in Slack Apps, send it a message (e.g. "Hi")
# 2. Bot replies with a pairing code in the terminal
# 3. Approve from the server:
openclaw pairing approve slack <YOUR_CODE>

# 4. Invite to channels:
# In Slack: /invite @OpenClaw in the target channel
```

#### Token Storage
- Slack tokens: store in environment variables — **never** hardcode in config files
- Gateway token: `~/.openclaw/openclaw.json` (file permissions below)

```bash
# In ~/.bashrc or ~/.profile
export OPENCLAW_SLACK_BOT_TOKEN="xoxb-..."
export OPENCLAW_SLACK_APP_TOKEN="xapp-..."
```

---

### 3. File System Permissions

```bash
# Lock down workspace and config
chmod 700 ~/.openclaw/workspace
chmod 600 ~/.openclaw/openclaw.json
```

---

### 4. MCP-First Execution Protocol

From `MCP_CHECKLIST.md` — the agent **must** use MCP tools rather than direct shell execution wherever available. This is a hard security rule:

> **When you try to do something directly (exec, read, write, shell) → FIRST check if MCP is available for that task.**

**Why this matters:**
- MCP tools have fixed, reviewed paths — no PATH injection risk
- Environment variables (license, library paths) are set inside the server — not exposed in shell history
- Errors are parsed and sanitized before being returned to the AI

**Registered MCP servers that replace direct shell calls:**

| Task | Direct shell (avoid) | MCP tool (use instead) |
|---|---|---|
| Flash bitstream | `openFPGALoader ...` | `flash_bitstream` |
| Synthesize | `gw_sh build.tcl` | `synthesize` |
| Full build | manual TCL + flash | `build` |
| Check USB | `lsusb` | `check_usb_devices` |
| Vault notes | `cat`, `grep` on files | `obsidian-vault` MCP |

---

### 5. Agent Path Safety Rules

From `Paths_Reference.md` — hard rules for the AI agent operating on this system:

1. **NEVER guess file paths** — always confirm with `find` before operating
2. **NEVER create a file if the canonical location is missing** — report to user first
3. **Canonical project paths** live in `Paths_Reference.md` in the vault — read it before any FPGA/LLM session

**Canonical active project paths:**

| Project | Canonical Path |
|---|---|
| Musical LED (Tang Mega 138K) | `/home/snit/ai/projects/ldpc/aChipDC/musical_letters/eda_proc/` |
| aiChipDC (AI Chip Design Center) | `/home/snit/ai/projects/ldpc/aChipDC/aiChipDC` |
| Research workspace root | `/home/snit/ai` |

---

### 6. Hard Operational Constraints

From `Path-Verification-Log.md` — the following constraints are permanently active in the agent's operating rules:

| Constraint | Rule |
|---|---|
| **Manifest Authority** | Canonical paths from `Paths_Reference.md` take precedence over any assumed path |
| **No Silent Delete** | Never delete files without explicit user confirmation — use `trash` over `rm` |
| **Sequential Operations** | Do not run parallel file operations — one operation completes before the next starts |
| **No Parallel Path Creation** | Never create multiple path variants simultaneously — one canonical path per resource |

---

### 7. Obsidian Vault Backup Security

From `add Obsidian.md` — the vault is sensitive research data. Back it up to a **private** repository:

```bash
# Clone to private GitHub repo (one-time setup)
git clone https://github.com/YOUR_ORG/private-vault.git \
    /home/snit/ai/obsidian-noted/openclaw-second-brain

# Configure git credential caching (avoid PAT prompts)
git config --global credential.helper store
```

**Authentication options (in order of preference):**
1. **SSH keys** — most secure, no token exposure
2. **Personal Access Token (PAT)** — `repo` scope only; generate at GitHub → Settings → Developer settings → Personal access tokens
3. Never use your GitHub password directly

**Obsidian Git plugin settings:**
- Enable `Pull on startup`
- Set backup interval: 5–15 minutes
- Repository must be **Private** — vault contains personal context and project IP

---

### 8. Model Resilience and Fallback

From `2026-04-27-Slack-OpenClaw-LLM-Fix.md` — the remote model endpoint can time out (Slack WebSocket also disconnects periodically). The system has a local fallback:

**Primary:** `vllm/Qwen/Qwen3.6-27B` at `https://aicenter.mahidol.ac.th/qwen3-6-27b/v1`  
**Fallback:** `ollama/qwen3.6:27b` at `http://localhost:11434/v1` (dual-GPU: RTX 3080 + RTX 3080 Ti)

Switch to local fallback:
```bash
openclaw config set agents.defaults.model.primary "ollama/qwen3.6:27b"
openclaw gateway restart
```

Switch back to remote:
```bash
openclaw config set agents.defaults.model.primary "vllm/Qwen/Qwen3.6-27B"
openclaw gateway restart
```

---

### 9. Disable Unused Channels

Reduce attack surface by disabling channels not in active use:

```yaml
# ~/.openclaw/openclaw.json — disable inactive channels
plugins:
  entries:
    telegram:
      enabled: false
    discord:
      enabled: false
```

---

### 10. Rate Limiting (Recommended for Shared Lab Use)

```bash
openclaw config set gateway.rateLimit.enabled true
openclaw config set gateway.rateLimit.maxRequests 100
openclaw config set gateway.rateLimit.windowMs 60000
```

---

## Troubleshooting

### FPGA / USB Issues

| Symptom | Cause | Fix |
|---|---|---|
| "No Gowin devices found" | BL616 not in JTAG mode | Press DBG_BOOT while plugging USB |
| "unable to open ftdi device" | Same as above | Same fix |
| `lsusb` shows `1a86:fe0c` but not `0403:6010` | BL616 in CDC mode | Press DBG_BOOT |
| "Permission denied" on USB | Missing udev rules | Run `install_udev_rules` via agent or manually |
| `programmer_cli` finds cable but not device | Wrong DIP switch or JTAG not active | Set all DIP OFF + DBG_BOOT |
| SRAM load fails | Flash is empty | Use `-f` flag to write flash first |

### Build Issues

| Symptom | Fix |
|---|---|
| Synthesis timeout (>5 min) | Check `LM_LICENSE_FILE`, verify license server is reachable |
| "Cannot find Qt platform" | `QT_QPA_PLATFORM=offscreen` not set — MCP server sets it automatically |
| "No .fs found in output/" | P&R failed silently — check agent's full stderr output |

### OpenClaw / MCP Issues

```bash
openclaw gateway restart
openclaw mcp show gowin-workflow
uv run python /media/snit/AiHPC/tools/vlsi/gowin/mcp_server.py  # test manually
openclaw logs --tail 50
```

### Model Endpoint Issues

```bash
curl https://aicenter.mahidol.ac.th/qwen3-6-27b/v1/models

# Fall back to local Ollama
openclaw config set agents.defaults.model.primary "ollama/qwen3.6:27b"
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  MAHIDOL FPGA AI WORKFLOW — QUICK REFERENCE             │
├─────────────────────────────────────────────────────────┤
│  START:       openclaw gateway start                    │
│  STATUS:      openclaw gateway status                   │
│  WEB CHAT:    http://localhost:18789                    │
│  SLACK:       #all-openclaw-ws                          │
├─────────────────────────────────────────────────────────┤
│  BOARD SETUP:                                           │
│    DIP:       All switches OFF                          │
│    JTAG:      Hold DBG_BOOT → plug USB → release        │
│    VERIFY:    lsusb | grep 0403:6010                    │
├─────────────────────────────────────────────────────────┤
│  AGENT COMMANDS (natural language):                     │
│    "Build and flash [project path]"                     │
│    "Synthesize [project path]"                          │
│    "Flash [bitstream.fs] to SRAM"                       │
│    "Detect FPGA"                                        │
│    "Check USB devices"                                  │
│    "What's the DIP switch config?"                      │
│    "Search my notes for [topic]"                        │
├─────────────────────────────────────────────────────────┤
│  LICENSE:     YOUR_LICENSE_SERVER                           │
│  MODEL:       Qwen3.6-27B @ aicenter.mahidol.ac.th     │
│  VAULT:       ~/ai/obsidian-noted/openclaw-second-brain │
└─────────────────────────────────────────────────────────┘
```

---

*Built for transparent, on-premise AI-assisted hardware design.*  
**Mahidol University AI Center** × **OpenClaw** × **Anthropic Claude** × **Qwen3.6-27B**
