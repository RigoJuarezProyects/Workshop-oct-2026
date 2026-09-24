# Local LLM Workshop

Welcome! In this workshop you'll install [Ollama](https://ollama.com), download two small
open-source language models, and chat with them from a simple Python script — all running
**100% locally on your laptop**, with no internet needed once the models are downloaded and
no API keys or accounts required.

You'll try:
- **Llama 3.2 (3B)** — Meta's small, fast general-purpose chat model (~2.0 GB)
- **Qwen 2.5 (3B)** — Alibaba's small, fast general-purpose chat model (~1.9 GB)

By the end, you'll be able to run both models and compare how they answer the same question.

## What you'll need

- A laptop (Mac or Windows) with at least **8 GB of RAM** and **8 GB of free disk space**
- Python 3.9 or newer
- About 15-20 minutes of download time (depends on wifi)

No GPU is required — these models run fine on CPU.

---

## Step 1: Install Ollama

Ollama is the program that downloads and runs LLMs locally, and exposes them to your
scripts through a small local server on your machine (`http://localhost:11434`).

### macOS

1. Go to https://ollama.com/download and download the macOS installer, **or** run this in
   Terminal:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Verify the install:
   ```bash
   ollama --version
   ```
   You should see output like `ollama version is 0.x.x`.

### Windows

1. Go to https://ollama.com/download and download **OllamaSetup.exe**.
2. Run the installer (no admin rights should be required — it installs to your user
   profile). Ollama will start automatically and show an icon in your system tray.
3. Verify the install by opening **PowerShell** or **Command Prompt** and running:
   ```powershell
   ollama --version
   ```
   You should see output like `ollama version is 0.x.x`.

> If `ollama` isn't recognized after installing, close and reopen your terminal window —
> the installer updates your PATH, which existing terminal sessions won't pick up.

---

## Step 2: Pull the two models

With Ollama installed and running (it runs automatically in the background after install),
pull both models. This is the part that takes the longest (a few minutes each, depending on
wifi), so start it as soon as you can:

```bash
ollama pull llama3.2
ollama pull qwen2.5
```

Expected output ends with something like:
```
success
```

Confirm both models are present:
```bash
ollama list
```
You should see both `llama3.2` and `qwen2.5` listed with their size (~2 GB each).

---

## Step 3: Get the workshop code

Clone this repository (or download it as a ZIP from GitHub and extract it):

```bash
git clone https://github.com/<your-org>/llm-workshop.git
cd llm-workshop
```

Create a virtual environment and install the one Python dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows (PowerShell/cmd)

pip install -r requirements.txt
```

You should see `ollama` installed with no errors.

---

## Step 4: Run the chat script

```bash
python chat.py
```

You'll be asked to pick a model:

```
Which model would you like to talk to?
  1) llama3.2  (Meta, ~2.0 GB)
  2) qwen2.5   (Alibaba, ~1.9 GB)
Enter 1 or 2:
```

Type `1`, press Enter, then type a question, e.g.:

```
You: What's a fun fact about octopuses?
```

You should see the model's response stream in word-by-word.

**Try this:** type `switch` at any `You:` prompt to change models mid-session, and ask the
same question to both models to compare their answers. Type `exit` (or press Ctrl+C) to
quit.

---

## Workshop flow (what we'll do together, ~50 minutes)

| Time | Activity |
|---|---|
| 0-5 min | Intro: what is a local LLM, why run locally (privacy, cost, offline) |
| 5-10 min | Live instructor demo (projected) |
| 10-15 min | Everyone installs Ollama (Step 1) — pair up with your neighbor if you get stuck |
| 15-25 min | Everyone pulls both models (Step 2) — this runs in the background while we talk |
| 25-30 min | Clone the repo and install dependencies (Step 3), quick walkthrough of `chat.py` |
| 30-38 min | Everyone runs `chat.py` and gets a response from both models (Step 4) |
| 38-45 min | Open exploration: try creative prompts, compare model answers, share with the group |
| 45-50 min | Wrap-up, bonus exercise, Q&A |

If you get stuck at any point, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or raise your
hand — pairing up with a neighbor on the other OS is a great way to compare notes.

Finished early? Try the [bonus exercise](BONUS.md).

Laptop really can't run this? See the [cloud fallback appendix](docs/cloud-fallback.md).

## License

This workshop's code and materials are released under the [MIT License](LICENSE).
