from flask import Blueprint, render_template

pronunciation_bp = Blueprint("pronunciation", __name__, url_prefix="/pronunciation")

PRONUNCIATION_PRACTICE_ITEMS = [
    {
        "phrase": "Good morning, my name is Priya.",
        "tamil": "காலை வணக்கம், என் பெயர் பிரியா.",
        "phonetics": "gud MOR-ning, my naym iz PREE-yah",
        "focus_sounds": "/g/ in Good, /m/ in Morning, short /i/ in is",
        "tip": "Keep the 'oo' sound in 'Good' short. Do not stretch it like 'Gooood'."
    },
    {
        "phrase": "Could you please give me a bottle of water?",
        "tamil": "தயவுசெய்து எனக்கு ஒரு பாட்டில் தண்ணீர் தர முடியுமா?",
        "phonetics": "kud yoo pleez giv mee uh BOT-ul ov WAH-tur",
        "focus_sounds": "Silent 'l' in Could, /z/ sound in please, /v/ in give",
        "tip": "The letter 'l' in 'Could' is completely silent! Pronounce it like 'kud'."
    },
    {
        "phrase": "I am studying computer science in college.",
        "tamil": "நான் கல்லூரியில் கணினி அறிவியல் படித்து வருகிறேன்.",
        "phonetics": "I am STUH-dee-ing kum-PYOO-tur SY-unss in KOL-ij",
        "focus_sounds": "Soft /dʒ/ in college, /s/ in science",
        "tip": "Pronounce 'college' as 'KOL-ij' with a soft 'j' sound at the end, not 'col-lay-jee'."
    },
    {
        "phrase": "Where is the central railway station?",
        "tamil": "மத்திய ரயில் நிலையம் எங்குள்ளது?",
        "phonetics": "wair iz thuh SEN-trul RAYL-way STAY-shun",
        "focus_sounds": "/w/ vs /v/, /ʃ/ 'sh' sound in station",
        "tip": "Round your lips for 'Where' (/w/). Avoid pronouncing it with teeth like 'Vhere'."
    },
    {
        "phrase": "Thank you very much for your kind help.",
        "tamil": "உங்கள் அன்பான உதவிக்கு மிக்க நன்றி.",
        "phonetics": "thangk yoo VER-ee much for yoor kynd help",
        "focus_sounds": "Voiceless /θ/ in Thank, /v/ in very",
        "tip": "Put the tip of your tongue lightly between your teeth to make the soft 'Th' sound in Thank."
    },
    {
        "phrase": "Consistency is the key to fluent English.",
        "tamil": "தொடர் பயிற்சியே சரளமான ஆங்கிலத்திற்கு திறவுகோல்.",
        "phonetics": "kun-SIS-tun-see iz thuh kee too FLOO-unt ING-glish",
        "focus_sounds": "Stress on -SIS-, /f/ in fluent",
        "tip": "Place gentle emphasis on the second syllable of con-SIS-ten-cy."
    }
]

@pronunciation_bp.route("/")
def index():
    return render_template(
        "pronunciation.html",
        practice_items=PRONUNCIATION_PRACTICE_ITEMS
    )
