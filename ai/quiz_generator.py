import json
import random
from typing import List, Dict, Any
from config import Config

class QuizGenerator:
    """
    Generates balanced 10-question MCQ quizzes with instant scoring and bilingual feedback.
    Draws from curated question bank or live AI adapters.
    """

    def __init__(self, provider_adapter=None):
        self.provider_adapter = provider_adapter
        self.questions_bank = self._load_questions()

    def _load_questions(self) -> List[Dict[str, Any]]:
        quiz_file = Config.DATA_DIR / "quiz_questions.json"
        if quiz_file.exists():
            with open(quiz_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def generate_quiz(self, category: str = "Comprehensive", count: int = 10) -> List[Dict[str, Any]]:
        """
        Generates a 10-question quiz covering all 5 core modules or a specific category.
        """
        if self.provider_adapter and self.provider_adapter.is_available():
            ai_questions = self.provider_adapter.generate_quiz_questions(category, count)
            if ai_questions and len(ai_questions) >= count:
                return ai_questions[:count]

        # Offline / Curated Bank Fallback
        pool = self.questions_bank
        if category and category.lower() != "comprehensive":
            filtered = [q for q in pool if q.get("category", "").lower() == category.lower()]
            if filtered:
                pool = filtered

        # Ensure representation across categories if Comprehensive
        if category.lower() == "comprehensive" and len(pool) >= count:
            categories = ["Vocabulary", "Grammar", "Translation", "Sentence Correction", "Conversation"]
            selected = []
            for cat in categories:
                cat_questions = [q for q in pool if q.get("category") == cat]
                if cat_questions:
                    selected.extend(random.sample(cat_questions, min(2, len(cat_questions))))
            
            # Fill remaining if needed
            remaining_needed = count - len(selected)
            remaining_pool = [q for q in pool if q not in selected]
            if remaining_needed > 0 and remaining_pool:
                selected.extend(random.sample(remaining_pool, min(remaining_needed, len(remaining_pool))))
            
            random.shuffle(selected)
            return selected[:count]
        
        # Simple sample
        sample_size = min(count, len(pool))
        selected = random.sample(pool, sample_size)
        return selected

    def evaluate_quiz(self, questions: List[Dict[str, Any]], user_answers: Dict[str, int]) -> Dict[str, Any]:
        """
        Evaluates submitted answers, calculates score, and prepares detailed review object.
        """
        score = 0
        total = len(questions)
        results = []

        for idx, q in enumerate(questions):
            q_id = str(q.get("id", idx))
            submitted_idx = user_answers.get(q_id)
            correct_idx = q.get("correct_answer", 0)
            # Normalize submitted answer (support int, int string, or letter options 'A', 'B', 'C', 'D')
            is_correct = False
            if submitted_idx is not None:
                try:
                    if isinstance(submitted_idx, str) and submitted_idx.strip().upper() in ["A", "B", "C", "D"]:
                        letter_map = {"A": 0, "B": 1, "C": 2, "D": 3}
                        norm_sub = letter_map[submitted_idx.strip().upper()]
                    else:
                        norm_sub = int(submitted_idx)
                    is_correct = (norm_sub == int(correct_idx))
                except (ValueError, TypeError):
                    is_correct = False
            
            if is_correct:
                score += 1

            results.append({
                "question": q.get("question"),
                "category": q.get("category", "General"),
                "options": q.get("options", []),
                "user_answer": submitted_idx,
                "correct_answer": correct_idx,
                "is_correct": is_correct,
                "explanation_en": q.get("explanation_en", ""),
                "explanation_ta": q.get("explanation_ta", "")
            })

        answered_count = sum(1 for r in results if r.get("user_answer") is not None)
        percentage = round((score / total) * 100, 1) if total > 0 else 0.0
        is_completed = (answered_count >= total and total > 0)

        return {
            "total_questions": total,
            "answered_questions": answered_count,
            "score": score,
            "percentage": percentage,
            "is_completed": is_completed,
            "results": results
        }
