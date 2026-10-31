"""PSY144 2026 practice engine — original questions with traceable course evidence."""
from random import sample
from source_bank import _BANK, SOURCES

TOPICS = [
    {"id": "psychopathology", "name": "Psychopathology", "short": "Diagnosis, concepts & context", "tag": "TERM 3", "tone": "violet"},
    {"id": "poverty-ethnicity", "name": "Poverty & ethnicity", "short": "Social position and inequality", "tag": "TERM 4", "tone": "blue"},
    {"id": "culture-mental-health", "name": "Culture & mental health", "short": "Cultural meaning and assessment", "tag": "TERM 4", "tone": "mint"},
    {"id": "complementary-treatment", "name": "Complementary treatment", "short": "Evidence, ethics and support", "tag": "TERM 4", "tone": "amber"},
    {"id": "african-psychologies", "name": "African psychologies", "short": "Plural approaches and critique", "tag": "TERM 4", "tone": "rose"},
    {"id": "positive-psychology", "name": "Africa-centred well-being", "short": "Well-being in context", "tag": "TERM 4", "tone": "cyan"},
]


_QUESTION_BY_ID = {question["id"]: question for question in _BANK}
_TOPIC_IDS = {topic["id"] for topic in TOPICS}


def get_questions(topic_id: str, count: int = 5, mode: str = "medium") -> list[dict]:
    if topic_id not in _TOPIC_IDS:
        raise ValueError("Unknown topic")
    if mode not in ("medium", "hard"):
        raise ValueError("Unknown difficulty mode")
    if not 1 <= count <= 20:
        raise ValueError("Count must be between 1 and 20")
    available = [q for q in _BANK if q["topic_id"] == topic_id and q["mode"] == mode]
    selected = sample(available, min(count, len(available)))
    fields = ("id", "topic_id", "prompt", "choices", "difficulty", "mode", "source")
    return [{key: question[key] for key in fields} for question in selected]


def grade_answer(question_id: str, answer_index: int) -> dict:
    question = _QUESTION_BY_ID.get(question_id)
    if question is None:
        raise ValueError("Unknown question")
    if isinstance(answer_index, bool) or not isinstance(answer_index, int) or not 0 <= answer_index <= 3:
        raise ValueError("Answer index must be between 0 and 3")
    return {
        "correct": answer_index == question["correct_index"],
        "correct_index": question["correct_index"],
        "mode": question["mode"],
        "explanation": question["explanation"],
        "source": question["source"],
    }
