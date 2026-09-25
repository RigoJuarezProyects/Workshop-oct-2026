# Bonus Exercise: Benchmark the Two Models

Finished early? Here's a ~10 minute extension that builds directly on `chat.py`.

## The challenge

Write a small script, `benchmark.py`, that:

1. Sends the **same 5 prompts** to both `llama3.2` and `qwen2.5:3b`.
2. Times how long each model takes to respond to each prompt.
3. Prints a simple comparison table at the end, e.g.:

```
Prompt                                   llama3.2 (s)   qwen2.5:3b (s)
----------------------------------------  -------------  --------------
What is the capital of France?                    1.42            1.18
Write a haiku about the ocean.                     2.05            1.87
...
```

**Hints:**
- You already know how to call a model from `chat.py` — reuse `ollama.chat(model=..., messages=[...])`.
- Use Python's built-in `time` module: record `time.time()` before and after the call, and
  subtract.
- You don't need streaming for this — a single non-streamed `ollama.chat(...)` call (leave
  out `stream=True`) is simpler to time, since it returns the full response at once.
- Keep the prompt list short (5 is plenty) so the benchmark itself doesn't take too long to
  run.

## Stretch goal

Once the basic benchmark works, try one of these:
- Also print the **response length** (word count) for each model, alongside the timing.
- Add a **system prompt** (e.g., `{"role": "system", "content": "You are a pirate."}` as the
  first message) and see how both models' answers change in style.

---

## Reference solution

<details>
<summary>Click to expand (try it yourself first!)</summary>

```python
#!/usr/bin/env python3
"""benchmark.py - Compare response time between llama3.2 and qwen2.5:3b."""

import time

import ollama

MODELS = ["llama3.2", "qwen2.5:3b"]

PROMPTS = [
    "What is the capital of France?",
    "Write a haiku about the ocean.",
    "Explain recursion in one sentence.",
    "Name three prime numbers.",
    "What year did the first Moon landing happen?",
]


def time_prompt(model: str, prompt: str) -> float:
    start = time.time()
    ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return time.time() - start


def main() -> None:
    results = {model: [] for model in MODELS}

    for prompt in PROMPTS:
        for model in MODELS:
            elapsed = time_prompt(model, prompt)
            results[model].append(elapsed)
            print(f"  {model}: {elapsed:.2f}s for '{prompt[:40]}...'")

    print("\nPrompt".ljust(42) + "".join(f"{m:>14}" for m in MODELS))
    print("-" * (42 + 14 * len(MODELS)))
    for i, prompt in enumerate(PROMPTS):
        row = prompt[:40].ljust(42)
        for model in MODELS:
            row += f"{results[model][i]:>13.2f}s"
        print(row)

    print("\nAverages:")
    for model in MODELS:
        avg = sum(results[model]) / len(results[model])
        print(f"  {model}: {avg:.2f}s average")


if __name__ == "__main__":
    main()
```

This reuses the exact same `ollama.chat()` call from `chat.py`, just without streaming and
wrapped in timing logic. Running it prints per-prompt timings plus a final comparison table
and averages — usually showing both 3B models responding in a similar (low single-digit
seconds) ballpark on typical laptop hardware, with small models like these it's common to see
qwen2.5:3b respond a bit faster or slower than llama3.2 depending on the machine.

</details>
