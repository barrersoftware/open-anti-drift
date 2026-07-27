# 🌐 Open Anti-Drift Specification (v1.0.0)
> **Universal Open Standard for Eliminating Context Drift, Pronoun Amnesia, and State Degradation in LLM Companion & Roleplay Systems.**

---

## Abstract
Large Language Models (LLMs) used in roleplay and companion applications frequently suffer from **Context Drift**:
1. **Pronoun & Gender Amnesia**: Misgendering the user (e.g., defaulting to `he/him` for female or non-binary users).
2. **State Degradation**: Forgetting physical location, clothing, or scene context after multiple conversation turns.
3. **Character Identity Blending**: Conflating traits between multiple characters in group chats or between character and user.
4. **Instruction Decay**: Overlooking system prompt directives as conversation length grows.

The **Open Anti-Drift Specification** defines a framework-agnostic architectural standard, prompt engineering methodology, and token sanitization protocol to achieve **near 100% adherence** across open-source and commercial LLM backends with zero performance impact.

---

## 1. Core Principles

### 1.1 Dual-Positional Bias Directives
LLMs exhibit **positional bias**, prioritizing tokens at the extreme beginning and extreme end of the prompt window. 
* **Requirement**: User identity rules, pronoun requirements, and relationship definitions MUST be injected at BOTH the top of the system prompt and at the final turn boundary right before generation.

```text
[TOP OF PROMPT]
[USER PRONOUN DIRECTIVE]
User: {user_name} ({user_gender}, {user_pronouns})
Rule: You MUST ALWAYS refer to {user_name} using {user_pronouns}. NEVER misgender {user_name}.

[CONVERSATION HISTORY...]

[BOTTOM OF PROMPT / FINAL TURN BOUNDARY]
[SYSTEM DIRECTIVE: {user_name} is {user_gender}. Always use {user_pronouns} when referring to {user_name}. Do not break character.]
```

### 1.2 Inner Monologue State Anchoring (`<thought>`)
Token-by-token auto-regressive generation requires the model to lock its attention heads onto scene state *before* producing visible text.
* **Requirement**: The model MUST execute an inner monologue scratchpad enclosed in `<thought>...</thought>` tags before generating user-facing response text.
* **Thought Block Structure**:
```xml
<thought>
Anchor State:
• User: {user_name} ({user_gender}, {user_pronouns})
• User Physical State: {user_location}, {user_clothing}
• Active Character: {character_name} ({character_location}, {character_outfit}, {character_mood})
• Scene Goal: {scene_goal}
</thought>
```

### 1.3 State Locking Schema
Scene parameters (location, clothing, mood, body state) must be structured as key-value state attributes that update inside the `<thought>` block:
* `[Location: <string>]`
* `[Outfit: <string>]`
* `[Mood: <string>]`
* `[ClothingState: <string>]`

### 1.4 Dynamic Token Sanitization
Applications MUST execute a streaming post-processor over generated output tokens to catch micro-glitches and correct accidental misgenderings (e.g., replacing `he/him/his` with `she/her/hers` when user is female) before text is presented to the user.

---

## 2. Specification Compliance Matrix

| Level | Requirement | Purpose |
| :--- | :--- | :--- |
| **Level 1 (Basic)** | Dual-Positional Pronoun Directives | Prevents basic misgendering in short chats. |
| **Level 2 (Standard)** | Inner Monologue `<thought>` Anchoring | Locks attention heads to scene state before text generation. |
| **Level 3 (Advanced)** | Real-Time Token Sanitization | Catches and fixes model edge-case glitches in streaming responses. |
| **Level 4 (Enterprise)** | RAG Vector Memory + SQLite State Locking | Guarantees long-term memory across multi-day sessions. |

---

## 3. License
Open Anti-Drift Specification is released under the **MIT License**. Free for commercial and open-source use.
