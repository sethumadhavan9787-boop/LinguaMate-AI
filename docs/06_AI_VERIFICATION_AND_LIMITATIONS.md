# DELIVERABLE 6: AI VERIFICATION AND LIMITATIONS REPORT
## Academic Limitations, Failure Modes, and Responsible Engineering in Language Education

### 1. Introduction
While Large Language Models (LLMs) provide scalable, conversational English tutoring, deploying them directly to beginner learners without pedagogical filters introduces serious educational risks. This report details the verified limitations, hallucination vulnerabilities, and mitigation strategies implemented in **LinguaMate AI**.

---

### 2. Verified AI Failure Modes & Observations

#### A. Over-Correction of Acceptable Informal & Regional Variants
- **Observation:** Standard AI models trained on formal corpora often flag harmless spoken English idioms or acceptable conversational ellipses as catastrophic grammar errors.
- **Pedagogical Harm:** Discourages beginner learners who need fluency confidence more than hyper-prescriptive grammar.
- **LinguaMate Mitigation:** System prompts explicitly instruct the AI: *"Do not mark acceptable informal usage as an error unless it creates grammatical incoherence. Distinguish errors from stylistic choices."*

#### B. Translation Mirroring & Machine Translation Blindspots
- **Observation:** General-purpose translation tools (such as Google Translate) often preserve source language grammatical errors when translating into Tamil (e.g. translating *"Although he worked hard, but he failed"* directly into *"அவர் கடினமாக உழைத்த போதிலும், ஆனால் அவர் தோல்வியடைந்தார்"*).
- **Pedagogical Harm:** Validates erroneous English structures in the student's mind through false symmetrical translation.
- **LinguaMate Mitigation:** LinguaMate uses a dedicated translation evaluation prompt and human-verified bilingual dictionaries rather than relying on uninspected raw translation APIs.

#### C. Hallucination of Grammatical Etymology
- **Observation:** When prompted for "why" a sentence is wrong, LLMs occasionally invent non-existent rules (e.g. claiming a preposition cannot end a sentence or confusing countability with gender).
- **LinguaMate Mitigation:** Negative prompt constraint: *"Do not invent grammar rules. If unsure, acknowledge uncertainty."* In offline mode, rule verification is grounded in verified grammatical regex parsers.

#### D. Over-Trust and Learner Passivity
- **Observation:** Beginners tend to view AI responses as infallible, leading to passive acceptance without cognitive engagement.
- **LinguaMate Mitigation:** Visual transparency badges showing provider status; interactive "Human Verification" toggle in the 3-Tool Comparison Lab; prominent "Report AI" buttons in every module.

---

### 3. Summary of LinguaMate AI Guardrails

```
+-------------------------------------------------------------------------+
|                  RESPONSIBLE AI GUARDRAIL PIPELINE                     |
+-------------------------------------------------------------------------+
  [User Sentence]
        |
        v
  [1. Curated Offline Rule Matcher] ---> Match Found? ---> Output Verified Rule
        |                                                     (100% Deterministic)
        v (No rule triggered)
  [2. System Prompt Guardrails]
      - Explicit A1-A2 Level Constraint
      - Mandated Simple Tamil Explanation (தமிழ் விளக்கம்)
      - Negative Constraint Against Invented Rules
      - Forced One-Question-at-a-Time Cadence
        |
        v
  [3. Self-Consistency Verification]
      - Multi-path internal check for ambiguities
        |
        v
  [4. Human-in-the-Loop Override]
      - Learner report button logs questionable outputs to SQLite
      - Teacher verification status on benchmark sentences
```

---

### 4. Conclusion
LinguaMate AI proves that AI can safely empower vernacular language learners only when wrapped in pedagogical constraints, mother-tongue explanations, offline fallbacks, and transparent human verification mechanisms.
