# 🌐 Open Anti-Drift Standard (`open-anti-drift`)
> **Universal Open-Source Framework, Prompt Specification, and Multi-Language Token Sanitizer for Eliminating Context Drift & Pronoun Amnesia in LLM Companion Applications.**

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/haven-ai/open-anti-drift)

---

## 🚀 Overview

Context Drift is the #1 problem in AI companion and roleplay software. As chat history grows, Large Language Models (LLMs) frequently:
* ❌ **Misgender Users**: Defaulting to `he/him` for female or non-binary users despite profile settings.
* ❌ **Lose Physical State**: Forgetting current room, outfit, or physical positioning.
* ❌ **Conflate Characters**: Mixing up character personalities in multi-companion scenes.
* ❌ **Degrade Context**: Forgetting core user facts after 10–15 messages.

`open-anti-drift` is a **framework-agnostic, open standard and polyglot toolkit** designed for **SillyTavern, JanitorAI, KoboldAI, LM Studio, Ollama, vLLM, Android, iOS, and Web apps** to achieve 100% context retention and zero pronoun drift.

---

## 🏛️ Repository Architecture

```
open-anti-drift/
├── SPECIFICATION.md           # Universal Specification (v1.0.0)
├── sanitizers/                # Real-Time Streaming Token Sanitizer Libraries
│   ├── python/                # Python package (FastAPI / vLLM / Ollama)
│   ├── typescript/            # TypeScript / Node.js / React / Next.js
│   ├── kotlin/                # Kotlin / Android JVM module
│   ├── csharp/                # .NET / C# ASP.NET Core & Unity
│   └── rust/                  # Rust crate / WASM high-throughput proxy
├── templates/                 # Prompt Engineering Directives & Systems
└── benchmarks/                # Automated Model Drift Evaluation Suite
    └── run_drift_eval.py      # 30-turn automated drift benchmark runner
```

---

## 🛠️ Quickstart

### 1. Python Token Sanitizer
```python
from sanitizers.python.anti_drift_sanitizer import AntiDriftSanitizer

sanitizer = AntiDriftSanitizer(user_name="Daniel", user_gender="female")

# Extract inner monologue thought block & visible text
result = AntiDriftSanitizer.extract_thought_block(llm_output)
clean_thought = result["thought"]
clean_text = sanitizer.sanitize_text(result["visible_text"])
```

### 2. TypeScript Token Sanitizer
```typescript
import { AntiDriftSanitizer } from './sanitizers/typescript/antiDriftSanitizer';

const sanitizer = new AntiDriftSanitizer("Daniel", "female");
const cleanText = sanitizer.sanitizeText(rawLlmStreamToken);
```

### 3. Automated Benchmark Evaluator
Run a 30-turn anti-drift stress test against any local or remote OpenAI-compatible server:
```bash
python benchmarks/run_drift_eval.py --api-url http://localhost:18799 --model default
```

---

## 📜 License
Released under the **MIT License**. Free for commercial and open-source use.
