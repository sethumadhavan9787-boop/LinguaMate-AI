from flask import Blueprint, render_template, request, jsonify, session
import uuid
from database.database import get_db_connection, log_mistake
from ai.conversation import ConversationEngine
from ai.provider_adapters import get_ai_adapter

conversation_bp = Blueprint("conversation", __name__, url_prefix="/conversation")
adapter = get_ai_adapter()
engine = ConversationEngine(provider_adapter=adapter)

@conversation_bp.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    
    current_topic = request.args.get("topic", "self_introduction")
    current_level = request.args.get("level", "Beginner")
    
    # Load topic starter
    topic_starter = engine.get_topic_starter(current_topic, current_level)
    
    # Load recent conversation history for this session and topic
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM conversation_messages 
        WHERE session_id = ? AND topic = ? 
        ORDER BY id ASC LIMIT 50
    """, (session["session_id"], current_topic))
    history = [dict(row) for row in c.fetchall()]
    conn.close()

    topics = [
        {"id": "self_introduction", "name": "Self-Introduction (சுய அறிமுகம்)"},
        {"id": "family", "name": "Family & Relationships (குடும்பம்)"},
        {"id": "college", "name": "College & Campus (கல்லூரி)"},
        {"id": "shopping", "name": "Shopping & Supermarket (கடை)"},
        {"id": "travel", "name": "Travel & Directions (பயணம் & வழிகள்)"},
        {"id": "food", "name": "Food & Restaurant (உணவகம்)"},
        {"id": "interview", "name": "Job Interview Practice (வேலை நேர்காணல்)"}
    ]

    return render_template(
        "conversation.html",
        topics=topics,
        current_topic=current_topic,
        current_level=current_level,
        topic_starter=topic_starter,
        history=history,
        provider_name=adapter.name
    )

@conversation_bp.route("/send", methods=["POST"])
def send_message():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    topic = data.get("topic", "self_introduction")
    level = data.get("level", "Beginner")
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    conn = get_db_connection()
    c = conn.cursor()

    # Fetch last 6 messages as conversation context
    c.execute("""
        SELECT sender, message FROM conversation_messages 
        WHERE session_id = ? AND topic = ? 
        ORDER BY id DESC LIMIT 6
    """, (session["session_id"], topic))
    recent_db = [dict(row) for row in c.fetchall()]
    recent_history = list(reversed([{"role": r["sender"], "content": r["message"]} for r in recent_db]))

    # Generate response
    response_data = engine.respond(
        user_message=user_message,
        topic=topic,
        level=level,
        conversation_history=recent_history
    )

    # Save user message
    c.execute("""
        INSERT INTO conversation_messages (session_id, topic, sender, message, corrected_message, tamil_explanation, simpler_sentence)
        VALUES (?, ?, 'user', ?, ?, ?, ?)
    """, (
        session["session_id"], topic, user_message, 
        response_data.get("corrected_sentence"), 
        response_data.get("tamil_explanation"), 
        response_data.get("simpler_sentence")
    ))

    # Save AI message
    c.execute("""
        INSERT INTO conversation_messages (session_id, topic, sender, message)
        VALUES (?, ?, 'ai', ?)
    """, (session["session_id"], topic, response_data.get("ai_response")))

    # If learner made a mistake, automatically record to mistake_log (preventing duplicates)
    if response_data.get("has_correction"):
        log_mistake(
            source="conversation",
            original_sentence=user_message,
            corrected_sentence=response_data.get("corrected_sentence", ""),
            mistake_category=response_data.get("mistake_category", "Grammar Error"),
            error_type="conversation_mistake",
            explanation_en=f"Correction from {topic.replace('_', ' ').title()} practice.",
            explanation_ta=response_data.get("tamil_explanation", ""),
            conn=conn
        )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "response": response_data
    })

@conversation_bp.route("/reset", methods=["POST"])
def reset_conversation():
    session_id = session.get("session_id")
    data = request.get_json() or {}
    topic = data.get("topic")

    if session_id:
        conn = get_db_connection()
        c = conn.cursor()
        if topic:
            c.execute("DELETE FROM conversation_messages WHERE session_id = ? AND topic = ?", (session_id, topic))
        else:
            c.execute("DELETE FROM conversation_messages WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    return jsonify({"success": True})
