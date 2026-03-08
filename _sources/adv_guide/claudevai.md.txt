# DevOps Engineering HPC & AI

**Author:** Snit Sanghlao
**AI Assistant:** Claude Opus 4.6 (Anthropic)

---

## Claude Code on Windows + Remote SSH to HPC

> **Setup Philosophy:** No module system — all tools installed locally in the user's home directory on the HPC. VS Code runs on your local Windows PC and connects to the HPC via Remote SSH, where Claude Code operates as a workspace-aware AI agent with direct access to the remote filesystem and terminal.

---

## Part 1: Local Windows Setup

### Step 1 — Install Git and VS Code

Open **PowerShell** or **Command Prompt** as Administrator:

```powershell
# Install Git for Windows (includes Git Bash)
winget install --id Git.Git -e --source winget

# Install Visual Studio Code
winget install --id Microsoft.VisualStudioCode -e --source winget
```

> **Important:** After installation, **restart your terminal** to ensure `git` is recognized in your `PATH`.

### Step 2 — Fix "Claude Code process exited with code 1"

If Claude Code cannot find Git Bash, you must manually point to the executable.

1. **Locate Bash:** Usually at `C:\Program Files\Git\bin\bash.exe`
2. **Set the environment variable:**
   - Open **Start Menu** → search **"Edit the system environment variables"**
   - Click **Environment Variables**
   - Under **User variables**, click **New**
     - **Variable name:** `CLAUDE_CODE_GIT_BASH_PATH`
     - **Variable value:** `C:\Program Files\Git\bin\bash.exe`
3. **Restart VS Code** completely.

---

## Part 2: How the Remote SSH Connection Works

When you use VS Code's **Remote - SSH** extension, VS Code splits itself into two halves:

| Component | Runs On | Role |
|-----------|---------|------|
| **UI Frontend** | Local Windows PC | Icons, menus, editor windows |
| **VS Code Server** | Remote HPC Host | File access, terminal, extensions |

Any extension you install while connected via SSH is installed **on the remote host**. This is exactly what we want — Claude Code needs to live where the code and compute resources are.

---

## Part 3: Connect VS Code to Your HPC

1. Install the **Remote - SSH** extension in VS Code.
2. Open the Command Palette (`Ctrl+Shift+P`) → select **Remote-SSH: Connect to Host...**
3. Enter your HPC connection string, e.g.:

```
username@hpc-login.university.ac.th
```

4. Authenticate (password, SSH key, or jump host as required by your site).

> **Tip:** For passwordless login, configure `~/.ssh/config` on your local machine:
>
> ```
> Host myhpc
>     HostName hpc-login.university.ac.th
>     User username
>     IdentityFile ~/.ssh/id_ed25519
>     ForwardAgent yes
> ```
>
> Then simply connect to `myhpc` from the Remote-SSH menu.

---

## Part 4: Install Node.js Locally on HPC (No Module System)

Since we are **not using a module system**, install Node.js directly into your home directory using **nvm** (Node Version Manager).

Open the integrated terminal in VS Code (which is now a shell on the HPC):

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# Reload shell configuration
source ~/.bashrc

# Install the latest LTS version of Node.js
nvm install --lts

# Verify
node --version
npm --version
```

> **Why nvm?** It installs everything under `~/.nvm/` — no root permissions needed, no module system dependency, and you can switch Node versions at will.

---

## Part 5: Install Claude Code on the HPC

With Node.js available, install the Claude Code CLI globally (within your nvm-managed prefix):

```bash
npm install -g @anthropic-ai/claude-code
```

Verify the installation:

```bash
claude --version
```

---

## Part 6: Install the VS Code Extension (Remote Side)

1. While connected to the HPC via Remote-SSH, open the **Extensions** view (`Ctrl+Shift+X`).
2. Search for **"Claude Code"** (by Anthropic).
3. Click **Install on SSH: \[your-hpc-name\]**.

> **Critical:** Do **not** install it only locally. Ensure it says **"Install on SSH"** so the extension logic runs on the remote host where the files and compute resources are.

---

## Part 7: Authenticate Claude Code

The first time you run `claude` in the terminal, it will provide an authentication URL:

```bash
claude
```

1. Copy the URL displayed in the terminal.
2. Open it in your **local PC browser**.
3. Sign in to your Anthropic account.
4. Copy the authentication code and paste it back into the VS Code terminal.

Your session is now authenticated and persists across reconnections.

---

## Part 8: The "Teleport" Feature

If you start a conversation on [claude.ai/code](https://claude.ai/code) (the web version), you can sync it directly into your HPC workspace:

```bash
claude --teleport
```

This pulls your web conversation history into the remote terminal session — useful for continuing research discussions seamlessly on the cluster.

---

## Important HPC Considerations

### Login vs. Compute Nodes

**Do not** run heavy Claude Code tasks (complex builds, large test suites, GPU workloads) on the login node. This can degrade the cluster for all users.

If your HPC uses Slurm, connect to a compute node via an interactive session:

```bash
# Request an interactive session with GPU
srun --partition=gpu --gres=gpu:1 --time=04:00:00 --pty bash

# Then run Claude Code inside this session
claude
```

Alternatively, configure VS Code Remote-SSH to connect directly to the allocated compute node.

### Internet Access

Claude Code must communicate with Anthropic's API servers. Some HPC compute nodes are firewalled from the external internet. Solutions:

- Run Claude Code from a **login node** or a node with outbound internet access (for the AI interaction part).
- Configure an **HTTP proxy** if your site provides one:

```bash
export HTTP_PROXY=http://proxy.university.ac.th:3128
export HTTPS_PROXY=http://proxy.university.ac.th:3128
```

### File System Awareness

Claude Code is workspace-aware. When installed on the remote host, it can directly:

- Read and navigate your project files on the HPC filesystem
- Access shared storage (Lustre, NFS, GPFS)
- Run commands in the HPC terminal
- Interact with job schedulers (Slurm, PBS)

---

## Quick Reference: Full Setup Checklist

```text
LOCAL WINDOWS PC                          REMOTE HPC HOST
─────────────────                         ────────────────
[1] Install Git (winget)                  [4] Install nvm + Node.js (~/.nvm/)
[2] Install VS Code (winget)              [5] npm install -g @anthropic-ai/claude-code
[3] Install Remote-SSH extension          [6] Install Claude Code VS Code extension
    + Set CLAUDE_CODE_GIT_BASH_PATH           (on SSH remote side)
                                          [7] Authenticate: claude → browser → paste code
```

---

## Architecture Diagram

```
┌─────────────────────────┐         SSH Tunnel          ┌──────────────────────────────┐
│   Local Windows PC      │◄──────────────────────────►│   HPC Host                    │
│                         │                             │                               │
│  VS Code (UI Frontend)  │                             │  VS Code Server               │
│  Remote-SSH Extension   │                             │  Claude Code CLI (~/.nvm/)    │
│  Git Bash               │                             │  Claude Code Extension        │
│                         │                             │  Project Files                │
│                         │    Anthropic API (HTTPS)    │  GPU / CPU Resources          │
│                         │         ┌───────────────────┤                               │
└─────────────────────────┘         │                   └──────────────────────────────┘
                                    ▼
                          ┌───────────────────┐
                          │  Anthropic Cloud   │
                          │  (Claude API)      │
                          └───────────────────┘
```

---

*Generated for DevOps & HPC AI workflows — local home-directory installation, no module system required.*
