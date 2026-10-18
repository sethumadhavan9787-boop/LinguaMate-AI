import random
from typing import Dict, Any, List
from .grammar_checker import GrammarChecker
from .prompt_templates import CONVERSATION_SYSTEM_PROMPT

class ConversationEngine:
    """
    Interactive conversation partner for Tamil-speaking beginners.
    Supports Beginner, Elementary, and Intermediate modes with bilingual explanations.
    """

    TOPIC_INTROS = {
        "self_introduction": {
            "title": "Self-Introduction (சுய அறிமுகம்)",
            "starter": "Hello! Welcome to our English practice. What is your name, and which town or village do you come from?",
            "simpler": "Hello! What is your name?",
            "follow_ups": [
                "Nice to know that! What subjects or degree are you studying in college?",
                "That sounds great! What do you like to do in your free time?",
                "Very interesting! Why are you interested in improving your English?"
            ]
        },
        "family": {
            "title": "Family and Relationships (குடும்பம்)",
            "starter": "Hello! Let's talk about your family today. How many members are there in your family?",
            "simpler": "How many people are in your family?",
            "follow_ups": [
                "Wonderful! Do you have any brothers or sisters?",
                "That is nice! What does your father or mother do?",
                "That sounds like a loving family! Who is your closest friend or relative?"
            ]
        },
        "college": {
            "title": "College and Campus Life (கல்லூரி வாழ்க்கை)",
            "starter": "Good day! How is your college experience so far? What department are you in?",
            "simpler": "What do you study in college?",
            "follow_ups": [
                "That is an exciting subject! Which professor's lecture do you enjoy the most?",
                "Do you usually travel by bus or bike to college?",
                "Have you participated in any sports or cultural club activities?"
            ]
        },
        "shopping": {
            "title": "Shopping and Supermarket (கடையில் வாங்குதல்)",
            "starter": "Welcome to our shop! How can I help you today? Are you looking for clothes or books?",
            "simpler": "Hello! What do you want to buy?",
            "follow_ups": [
                "We have high quality items here. What color or size do you prefer?",
                "This one is five hundred rupees. Would you like me to pack it for you?",
                "Will you pay by cash or UPI on your phone?"
            ]
        },
        "travel": {
            "title": "Travel and Directions (பயணம் மற்றும் வழிகள்)",
            "starter": "Excuse me! I am new to this town. Could you please tell me how to reach the nearest bus stand?",
            "simpler": "Where is the bus stand?",
            "follow_ups": [
                "Thank you! Is it within walking distance or should I take an auto rickshaw?",
                "Do express buses to Chennai stop there regularly?",
                "What is the average ticket fare for this trip?"
            ]
        },
        "food": {
            "title": "Food and Dining (உணவு மற்றும் உணவகம்)",
            "starter": "Good evening! Welcome to Hotel Saravana. What delicious South Indian food would you like to have?",
            "simpler": "What food do you want to eat?",
            "follow_ups": [
                "Excellent choice! Would you like crispy masala dosa or soft idlis?",
                "How would you like your filter coffee — hot with less sugar?",
                "Did you enjoy your meal? Can I bring the bill?"
            ]
        },
        "interview": {
            "title": "Job Interview Practice (வேலை நேர்காணல்)",
            "starter": "Good morning and welcome to your campus interview! Please introduce yourself and mention your key strengths.",
            "simpler": "Good morning! Tell me your name and degree.",
            "follow_ups": [
                "Very good! What was your role in your final year capstone project?",
                "Why do you want to join our organization as a junior software engineer?",
                "Where do you see yourself in the next two to three years?"
            ]
        }
    }

    def __init__(self, provider_adapter=None):
        self.grammar_checker = GrammarChecker(provider_adapter=provider_adapter)
        self.provider_adapter = provider_adapter

    def get_topic_starter(self, topic: str, level: str = "Beginner") -> Dict[str, Any]:
        info = self.TOPIC_INTROS.get(topic, self.TOPIC_INTROS["self_introduction"])
        starter_text = info["starter"]
        simpler_text = info["simpler"]
        
        if level == "Beginner":
            starter_text = info["starter"]
        elif level == "Intermediate":
            starter_text = f"{info['starter']} Please feel free to answer in 2 to 3 detailed sentences."
            
        return {
            "topic": topic,
            "title": info["title"],
            "starter": starter_text,
            "simpler": simpler_text,
            "tamil_note": "உங்கள் பதிலை எளிய ஆங்கிலத்தில் தட்டச்சு செய்யவும். தவறுகளைப் பற்றி கவலைப்பட வேண்டாம்!"
        }

    def respond(self, user_message: str, topic: str = "self_introduction", level: str = "Beginner", conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process user message, perform grammar correction with Tamil notes, and generate tutor response.
        """
        user_message = user_message.strip()
        if not user_message:
            return {
                "corrected_sentence": "",
                "has_correction": False,
                "tamil_explanation": "",
                "extra_example": "",
                "ai_response": "Please write a message to continue our conversation. தயவுசெய்து உங்கள் பதிலை எழுதுங்கள்.",
                "simpler_sentence": "",
                "follow_up_question": "What would you like to talk about?"
            }

        # Check grammar
        grammar_res = self.grammar_checker.check_sentence(user_message)
        has_correction = not grammar_res.get("is_correct", True)
        corrected_sentence = grammar_res.get("corrected", user_message)
        tamil_explanation = grammar_res.get("tamil_explanation", "")
        examples = grammar_res.get("examples", [])
        extra_example = examples[0] if examples else ""

        # Live Provider Adapter execution if enabled
        if self.provider_adapter and self.provider_adapter.is_available():
            live_res = self.provider_adapter.generate_conversation_reply(
                message=user_message,
                topic=topic,
                level=level,
                history=conversation_history or []
            )
            if live_res:
                return live_res

        # Curated Offline Tutor Response
        topic_info = self.TOPIC_INTROS.get(topic, self.TOPIC_INTROS["self_introduction"])
        follow_ups = topic_info["follow_ups"]
        
        # Pick relevant follow up
        history_len = len(conversation_history) if conversation_history else 0
        follow_up_idx = (history_len // 2) % len(follow_ups)
        next_question = follow_ups[follow_up_idx]

        # Encouraging tutor feedback
        if has_correction:
            encouragements = [
                "Good effort! I noticed a small grammar improvement above.",
                "Well said! Check the quick Tamil explanation above to polish your sentence.",
                "Nice try! Practicing this rule will make your English even stronger."
            ]
        else:
            encouragements = [
                "Excellent! That was clear, natural, and grammatically accurate.",
                "Great sentence! You expressed yourself very clearly.",
                "Wonderful! Your English is improving step by step."
            ]
        
        encouragement = random.choice(encouragements)
        full_reply = f"{encouragement} {next_question}"
        simpler_version = next_question.split('?')[0] + '?' if '?' in next_question else next_question

        return {
            "original_sentence": user_message,
            "corrected_sentence": corrected_sentence if has_correction else "",
            "has_correction": has_correction,
            "mistake_category": ", ".join(grammar_res.get("errors", [])) if has_correction else "",
            "tamil_explanation": tamil_explanation if has_correction else "உங்கள் வாக்கியம் சரியாகவும் தெளிவாகவும் உள்ளது!",
            "extra_example": extra_example,
            "ai_response": full_reply,
            "simpler_sentence": f"Simpler version: {simpler_version}",
            "follow_up_question": next_question
        }
