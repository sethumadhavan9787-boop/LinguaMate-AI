# DELIVERABLE 8: RESPONSIBLE AI AND ETHICAL FRAMEWORK
## Principles, Privacy Policies, and Safety Protocols for Vernacular AI Tutoring

### 1. Framework Purpose
Deploying Artificial Intelligence in educational contexts with vulnerable or beginner learners requires strict ethical guardrails. LinguaMate AI is built in accordance with UNESCO and ACM guidelines for Responsible AI in Education.

---

### 2. Eight Core Dimensions of Responsible AI in LinguaMate

#### 1. Cultural Nuance & Contextual Grounding
- **Ethical Mandate:** Language models trained predominantly on Western texts risk cultural alienation when teaching rural or vernacular learners.
- **Implementation:** LinguaMate’s exercises, examples, and vocabulary center on South Indian daily life: local cuisine (idli, sambar, filter coffee), public transit (town bus, railway station), joint and nuclear family dynamics, and collegiate campus placement environments.

#### 2. Dialect Awareness & Linguistic Respect
- **Ethical Mandate:** Non-standard regional varieties of English (e.g. Indian English) must not be treated with hostility or condescension.
- **Implementation:** The system distinguishes grammatical errors that impair comprehension from acceptable regional idioms. Polite explanations explain *why* international standard English prefers certain alternatives without invalidating the learner's home background.

#### 3. Translation Transparency & Avoiding Ambiguity
- **Ethical Mandate:** Literal word-for-word machine translation often introduces distorted semantic interpretations.
- **Implementation:** All core vocabulary and daily lessons feature curated, human-checked Tamil translations (தமிழ் விளக்கம்). The system highlights false cognates and structural mismatches between Tamil SOV and English SVO syntax.

#### 4. Mitigating AI Hallucinations
- **Ethical Mandate:** Generative AI models are prone to hallucinating facts, rules, or etymological origins when uncertain.
- **Implementation:** Strict system prompt guardrails instruct the model: *"Do not invent grammar rules. If unsure, acknowledge uncertainty."* In offline mode, grammar analysis is deterministic.

#### 5. Guarding Against Over-Trust
- **Ethical Mandate:** Beginners may treat AI tutors as infallible authorities.
- **Implementation:** Explicit notices accompany every generated explanation: *"AI is a practice assistant, not an unquestionable authority."* Students are encouraged to test and compare AI outputs in the 3-Tool Comparison Lab.

#### 6. Privacy by Design & Zero Data Extraction
- **Ethical Mandate:** Educational tools must never exploit student practice data or harvest personal information.
- **Implementation:** LinguaMate AI requires **no user registration**, **no email address**, **no phone number**, and **no cloud tracking**. All chat history, mistakes, and quiz scores remain stored locally on the user's machine in SQLite (`instance/linguamate.db`).

#### 7. Human-in-the-Loop Oversight
- **Ethical Mandate:** Teachers and learners must retain the agency to inspect, verify, and override AI conclusions.
- **Implementation:** The Three-Tool Comparison Lab allows human reviewers to mark outputs as *Verified*, *Uncertain*, or *Incorrect*.

#### 8. Accessible Reporting Pipeline
- **Ethical Mandate:** Any biased, inaccurate, or questionable AI output must have a frictionless reporting channel.
- **Implementation:** A global "Report AI" button is accessible across all modules. Logged reports are stored in the local audit table (`questionable_reports`) for transparency and quality improvement.

---

### 3. Ethical Pledge for College Capstone Evaluation
LinguaMate AI does not fabricate external API responses or misrepresent synthetic computer audio as human native recordings. Full architectural transparency is maintained across all features.
