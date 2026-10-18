# DELIVERABLE 10: VIVA VOCE AND DEMONSTRATION GUIDE
## Examiner Presentation Script and Defense Notes for LinguaMate AI

### 1. 5-Minute Demonstration Walkthrough Script

#### Step 1: System Boot & Dashboard (Minute 0:00 – 1:00)
- **Action:** Open terminal, execute `python app.py`, and launch `http://127.0.0.1:5000` in the browser.
- **Presenter Script:**
  > *"Good morning respected examiners. I present LinguaMate AI, an AI-powered language companion for Tamil-speaking beginners learning English. Our system runs 100% free and offline without mandatory API keys. On the dashboard, you can see our learning metrics: 14-day study plan progress, vocabulary words mastered, active streak, and Chart.js skill trajectory."*

#### Step 2: 14-Day Structured Study Plan (Minute 1:00 – 2:00)
- **Action:** Navigate to **2-Week Study Plan**, open **Day 1: Greetings and Introductions**.
- **Presenter Script:**
  > *"Rather than unstructured chat, beginners need a progressive curriculum. Each of our 14 daily lessons includes learning objectives, 10 vocabulary words with Tamil meanings, grammar explanations addressing L1 transfers, 5 model sentences with audio pronunciation, a speaking prompt, and 5 interactive practice questions."*
- **Action:** Click one practice question option to show immediate feedback and mark Day 1 complete.

#### Step 3: Bilingual AI Conversation & Grammar Lab (Minute 2:00 – 3:15)
- **Action:** Open **AI Conversation**, choose topic *"Self-Introduction"*, and type *"Myself Suresh from Salem"*.
- **Presenter Script:**
  > *"Here, the student types a common Indian English transfer error: 'Myself Suresh'. LinguaMate AI's tutor does not embarrass the student. It provides the polite correction: 'I am Suresh', offers a clear explanation in simple Tamil, presents a simpler sentence option, and asks a friendly follow-up question. Notice that this mistake is automatically saved to the Mistake Log for spaced review."*
- **Action:** Open **Grammar Lab**, click sample *"One of my friend is working in TCS company"*, and click **Check Grammar** to show discrete error badges and model sentences.

#### Step 4: Mandatory Capstone Feature: Three-Tool AI Comparison Lab (Minute 3:15 – 4:15)
- **Action:** Navigate to **3-Tool AI Lab**. Expand Case #1 (*"Myself Karthik, I am coming from Madurai"*).
- **Presenter Script:**
  > *"A core requirement of our capstone was evaluating free-tier AI tools. In this comparison lab, we compare OpenAI ChatGPT, Google Gemini, and Anthropic Claude across 10 benchmark sentences. Notice our audit findings: while all 3 models identify grammar rules, Google Gemini excels at native Tamil pedagogical explanations, while Claude excels at semantic nuances. We also cross-check against Google Translate, which often blindly mirrors grammatical errors into Tamil. Students can mark responses as Verified, Uncertain, or Incorrect."*

#### Step 5: Responsible AI & Automated Test Suite (Minute 4:15 – 5:00)
- **Action:** Show the **Responsible AI** page, demonstrate the **Report AI** modal, and show pytest test results.
- **Presenter Script:**
  > *"Finally, LinguaMate AI operates under Responsible AI principles: zero personal data collection, transparency badges, and an ethical reporting pipeline. Our automated test suite includes 23 unit tests with a 100% pass rate. Thank you, I am ready for questions."*

---

### 2. Viva Voce Examination Q&A Preparation

#### Q1: Why didn't you use paid APIs like GPT-4 API or ElevenLabs for this project?
**Answer:**
> *"A primary capstone requirement was building an application that costs zero dollars, requires no credit card, and remains usable by budget-constrained students. Paid TTS and LLM APIs exclude rural learners. LinguaMate AI uses a provider-independent architecture: by default, it runs completely offline using curated linguistic rules and the browser's native SpeechSynthesis API. It also supports free-tier API keys like Gemini and Groq if configured."*

#### Q2: How does LinguaMate handle L1 (Tamil) interference errors?
**Answer:**
> *"Tamil syntax is Subject-Object-Verb, lacks indefinite articles ('a/an'), and uses reflexive pronouns differently than English. Beginners frequently translate thoughts word-for-word, producing errors like 'Myself Suresh', 'yesterday night', or dropping articles. LinguaMate's rule engine and system prompts specifically target these L1 transfers, explaining the structural mismatch directly in simple Tamil."*

#### Q3: What is the difference between few-shot prompting and self-consistency in your Prompt Library?
**Answer:**
> *"Few-shot prompting provides the model with 2 to 3 concrete input-output examples before the task, which conditions the model to format answers strictly without hallucinating. Self-consistency generates multiple reasoning paths—such as prescriptive grammar, L1 transfer, and informal pragmatics—and compares them before outputting a verified result, preventing single-pass reasoning errors."*

#### Q4: How is data persisted across application restarts?
**Answer:**
> *"All lessons, 105 vocabulary words, quiz attempts, conversation history, mistake logs, and AI comparison evaluations are persisted in a local relational SQLite database (`instance/linguamate.db`). Parameterized queries are used exclusively to guarantee SQL injection safety."*

#### Q5: Can this application work if the internet is completely disconnected?
**Answer:**
> *"Yes. After the initial browser load of cached CDN scripts, the Python Flask backend, SQLite database, vocabulary library, 3D flashcards, grammar rule checker, 14-day study plan, quiz generator, and browser speech synthesis run 100% offline without any external internet connection."*
