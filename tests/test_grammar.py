import pytest
from ai.grammar_checker import GrammarChecker

@pytest.fixture
def checker():
    return GrammarChecker()

# Existing baseline tests
def test_myself_introduction_error(checker):
    res = checker.check_sentence("Myself Suresh, I am living in Salem.")
    assert res["is_correct"] is False
    assert "I am Suresh" in res["corrected"]
    assert "Myself" in res["tamil_explanation"]
    assert "L1 Transfer (Reflexive Pronoun)" in res["errors"]

def test_yesterday_night_error(checker):
    res = checker.check_sentence("Yesterday night he did not went to study.")
    assert res["is_correct"] is False
    assert "last night" in res["corrected"].lower()
    assert "Time Collocation (L1 Transfer)" in res["errors"]

def test_did_not_went_double_past(checker):
    res = checker.check_sentence("He did not went to college.")
    assert res["is_correct"] is False
    assert "did not go" in res["corrected"]
    assert "Auxiliary Verb & Double Past Tense" in res["errors"]

def test_one_of_my_friend_plural_concord(checker):
    res = checker.check_sentence("One of my friend is working in Chennai.")
    assert res["is_correct"] is False
    assert "one of my friends" in res["corrected"].lower()
    assert "Partitive Concord (Plural Noun)" in res["errors"]

def test_revert_back_redundancy(checker):
    res = checker.check_sentence("Please revert back to my email.")
    assert res["is_correct"] is False
    assert "reply" in res["corrected"].lower()
    assert "Tautology / Redundancy" in res["errors"]

def test_correct_sentence(checker):
    res = checker.check_sentence("I am a dedicated student.")
    assert res["is_correct"] is True
    assert res["status"] == "Correct"
    assert len(res["errors"]) == 0
    assert "இலக்கணப் பிழையும் கண்டறியப்படவில்லை" in res["tamil_explanation"]

# 1. Primary bug: "i will has book" -> "I will have a book."
def test_i_will_has_book_modal_and_article(checker):
    res = checker.check_sentence("i will has book")
    assert res["is_correct"] is False
    assert res["status"] == "Needs Correction"
    assert res["corrected"] == "I will have a book."
    assert "Modal Auxiliary & Base Verb" in res["errors"]
    assert "Missing Article / Determiner" in res["errors"]
    assert res["mistake_category"] != ""
    assert res["explanation_en"] != ""
    assert res["tamil_explanation"] != ""
    assert len(res["examples"]) >= 1
    assert "I will have a book." in res["examples"]

# 1. Modal verb grammar examples
def test_modal_verb_inflections(checker):
    # "She will goes to school" → "She will go to school."
    res1 = checker.check_sentence("She will goes to school")
    assert res1["is_correct"] is False
    assert res1["status"] == "Needs Correction"
    assert res1["corrected"] == "She will go to school."
    assert "Modal Auxiliary & Base Verb" in res1["errors"]
    assert "Base form" in res1["explanation_ta"] or "Modal" in res1["explanation_ta"]
    assert len(res1["examples"]) >= 1

    # "He can speaks English" → "He can speak English."
    res2 = checker.check_sentence("He can speaks English")
    assert res2["is_correct"] is False
    assert res2["status"] == "Needs Correction"
    assert res2["corrected"] == "He can speak English."
    assert "Modal Auxiliary & Base Verb" in res2["errors"]

    # "I should went home" → "I should go home."
    res3 = checker.check_sentence("I should went home")
    assert res3["is_correct"] is False
    assert res3["status"] == "Needs Correction"
    assert res3["corrected"] == "I should go home."
    assert "Modal Auxiliary & Base Verb" in res3["errors"]

    # "They must studies" → "They must study."
    res4 = checker.check_sentence("They must studies")
    assert res4["is_correct"] is False
    assert res4["status"] == "Needs Correction"
    assert res4["corrected"] == "They must study."
    assert "Modal Auxiliary & Base Verb" in res4["errors"]

# 2. Articles and determiners examples
def test_articles_and_determiners(checker):
    # "I have book" → "I have a book."
    res1 = checker.check_sentence("I have book")
    assert res1["is_correct"] is False
    assert res1["status"] == "Needs Correction"
    assert res1["corrected"] == "I have a book."
    assert "Missing Article / Determiner" in res1["errors"]
    assert "Article" in res1["explanation_ta"]

    # "She is teacher" → "She is a teacher."
    res2 = checker.check_sentence("She is teacher")
    assert res2["is_correct"] is False
    assert res2["status"] == "Needs Correction"
    assert res2["corrected"] == "She is a teacher."
    assert "Missing Article / Determiner" in res2["errors"]

# 3. Preserve correct sentences unchanged
@pytest.mark.parametrize("valid_sentence", [
    "I will have a book.",
    "She will go to school.",
    "He can speak English.",
    "I have a book.",
    "Water is important."
])
def test_valid_sentences_preserved(checker, valid_sentence):
    res = checker.check_sentence(valid_sentence)
    assert res["is_correct"] is True
    assert res["status"] == "Correct"
    assert res["corrected"] == valid_sentence
    assert len(res["errors"]) == 0
    assert "இலக்கணப் பிழையும் கண்டறியப்படவில்லை" in res["tamil_explanation"]
