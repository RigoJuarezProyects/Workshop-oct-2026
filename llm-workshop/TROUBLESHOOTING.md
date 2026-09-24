# Troubleshooting

Quick fixes for the most common issues during the workshop, organized by the step in
[README.md](README.md) where they tend to show up.

## Installing Ollama

| Symptom | Likely cause | Fix |
|---|---|---|
| `ollama: command not found` (macOS) or `'ollama' is not recognized...` (Windows) | Terminal was opened before Ollama finished installing, or PATH wasn't refreshed | Close and reopen your terminal window, then try `ollama --version` again. On Windows, you can also just restart the terminal app entirely. |
| macOS install script fails with a permissions error | Corporate/managed laptop restricting script execution | Use the `.dmg` installer from https://ollama.com/download instead of the `curl \| sh` one-liner. |
| Windows installer seems to hang or asks for admin rights unexpectedly | Some corporate security software intercepts installers | Try running the installer again; if it still fails, use the [cloud fallback](docs/cloud-fallback.md) — ask the instructor. |
| `ollama --version` shows a version but `ollama list` hangs forever | Ollama background service isn't running | macOS: check for the llama icon in the menu bar; if missing, relaunch the Ollama app once from Applications. Windows: check the system tray for the Ollama icon; if missing, relaunch Ollama from the Start menu. |

## Pulling the models

| Symptom | Likely cause | Fix |
|---|---|---|
| `ollama pull llama3.2` fails partway with a network/timeout error | Flaky venue wifi | Just re-run the same `ollama pull` command — it resumes from where it left off, it doesn't restart from zero. |
| Pull is extremely slow (many minutes with no progress) | Congested shared wifi (common with a full room downloading ~2 GB each at once) | Be patient — this is expected on conference/classroom wifi. Pair up with a neighbor who has finished, or ask the instructor about the [cloud fallback](docs/cloud-fallback.md). |
| `Error: pull model manifest: file does not exist` | Typo in the model name | Double check spelling: it's `llama3.2` and `qwen2.5` (no spaces, exact tag names). Run `ollama list` to see what's already pulled. |
| Pull fails with a disk space error | Not enough free space (each model is ~2 GB, so ~4-5 GB free is needed for both plus overhead) | Free up disk space (empty trash, clear downloads) and retry. |

## Running chat.py

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'ollama'` | Dependencies not installed, or venv not activated | Make sure you ran `pip install -r requirements.txt` **inside** the activated virtual environment. Re-activate with `source .venv/bin/activate` (macOS) or `.venv\Scripts\activate` (Windows), then reinstall. |
| `python: command not found` (macOS) | Some Macs only ship `python3`, not `python` | Use `python3 chat.py` instead of `python chat.py`. |
| Script hangs at "Now chatting with..." with no response | Ollama background service stopped, or model isn't actually pulled | In a separate terminal, run `ollama list` to confirm the model is present, and `ollama ps` to see if anything is currently loaded. Restart the Ollama app/service if needed. |
| `[Error talking to Ollama: model 'llama3.2' not found]` with a 404 | Model wasn't pulled successfully (partial/failed download) | Run `ollama pull llama3.2` (or `qwen2.5`) again and confirm it ends with `success`, then re-run `chat.py`. |
| `Address already in use` or similar when starting Ollama manually | Another Ollama process is already running on port 11434 | This is usually fine — Ollama runs as a background service, you don't need to start it manually. If you did start it manually and see this, just skip that step; the existing service is already up. |
| Responses are extremely slow (many seconds per word) | Laptop is low on free RAM (many other apps open) | Close other heavy apps (browser tabs, IDEs) to free up RAM. Both models are small but still need ~4-6 GB of free RAM to run smoothly. |
| Typing `switch` or `exit` seems to do nothing | Accidentally sent as a "message" mid-response, or extra whitespace | Wait for the current response to finish printing, then type `switch` or `exit` on its own at the `You:` prompt. |

## General checks

- **Is Ollama running at all?** Run `ollama list` in a terminal — if this works and shows your
  models, the background service is healthy.
- **Is a model actually loaded?** Run `ollama ps` to see which models are currently active in
  memory.
- **Still stuck?** Pair up with a neighbor on the other OS (Mac/Windows) — many issues are
  OS-specific and a second pair of eyes helps fast. Otherwise, raise your hand for the
  instructor.
