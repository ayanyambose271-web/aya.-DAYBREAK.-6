"""DAYBREAK demo question bank and grading engine.

The bank contains original sample questions, not course-source-grounded exam items.
Swap it for verified material before using this as a serious revision tool.
"""
from random import sample
from difficulty_bank import NEW_QUESTIONS

TOPICS = [
    {"id": "psychopathology", "name": "Psychopathology", "short": "Diagnosis, concepts & context", "tag": "TERM 3", "tone": "violet"},
    {"id": "poverty-ethnicity", "name": "Poverty & ethnicity", "short": "Social position and inequality", "tag": "TERM 4", "tone": "blue"},
    {"id": "culture-mental-health", "name": "Culture & mental health", "short": "Cultural meaning and assessment", "tag": "TERM 4", "tone": "mint"},
    {"id": "complementary-treatment", "name": "Complementary treatment", "short": "Evidence, ethics and support", "tag": "TERM 4", "tone": "amber"},
    {"id": "african-psychologies", "name": "African psychologies", "short": "Plural approaches and critique", "tag": "TERM 4", "tone": "rose"},
    {"id": "positive-psychology", "name": "Africa-centred well-being", "short": "Well-being in context", "tag": "TERM 4", "tone": "cyan"},
]

# Each item uses a consistent 4-option multiple-choice structure.
_BANK = [
    {"id": "psy-001", "topic_id": "psychopathology", "difficulty": "Applied", "prompt": "Two students report similar symptoms, but only one has significant disruption in daily functioning. What is the best conclusion?", "choices": ["Both must have the same disorder", "Clinical assessment considers distress, impairment and context, not symptoms alone", "Symptoms never matter for diagnosis", "The student with less impairment is exaggerating"], "correct_index": 1, "explanation": "Assessment considers the pattern, duration, distress or impairment, relevant context and possible alternative explanations. Symptoms alone rarely settle a diagnosis."},
    {"id": "psy-002", "topic_id": "psychopathology", "difficulty": "Conceptual", "prompt": "Why is it inaccurate to define all unusual behaviour as psychological disorder?", "choices": ["Unusual behaviour is always healthy", "Only biological explanations are valid", "Unusual does not automatically imply distress, dysfunction or disorder", "Diagnosis depends entirely on social popularity"], "correct_index": 2, "explanation": "Statistical rarity and psychological disorder are not interchangeable. Clinical significance and cultural context matter."},
    {"id": "pov-001", "topic_id": "poverty-ethnicity", "difficulty": "Applied", "prompt": "A learner experiences chronic stress because of insecure housing and unequal access to services. Which explanation best avoids blaming the individual?", "choices": ["Structural conditions may shape exposure to stress", "The learner must lack motivation", "Ethnicity alone determines mental health", "Housing conditions have no relevance to well-being"], "correct_index": 0, "explanation": "Social determinants such as housing, services and economic insecurity can structure stress exposure and access to support."},
    {"id": "pov-002", "topic_id": "poverty-ethnicity", "difficulty": "Critical", "prompt": "A report compares mental health outcomes by ethnicity without measuring income or access to care. What is its main limitation?", "choices": ["It has too many possible explanations", "Ethnicity can never be studied", "Income proves all outcomes are biological", "It may confuse social inequality with ethnic-group differences"], "correct_index": 3, "explanation": "Group comparisons need careful attention to confounding factors, historical inequalities and how categories are constructed."},
    {"id": "cul-001", "topic_id": "culture-mental-health", "difficulty": "Applied", "prompt": "A clinician interprets a culturally meaningful expression of distress as inherently pathological. What was overlooked?", "choices": ["Cultural context in the meaning of symptoms", "The importance of faster diagnosis", "The need to ignore the client", "The claim that culture removes all suffering"], "correct_index": 0, "explanation": "The meaning and expression of distress may vary across contexts. Culturally informed assessment avoids automatic pathologisation."},
    {"id": "cul-002", "topic_id": "culture-mental-health", "difficulty": "Conceptual", "prompt": "What is a key principle of culturally responsive mental-health care?", "choices": ["Apply one fixed explanation to every client", "Avoid discussing values or beliefs", "Explore the client's framework without assuming everyone in a group thinks alike", "Replace all evidence with stereotypes"], "correct_index": 2, "explanation": "Cultural responsiveness involves curiosity, humility and individual assessment rather than treating cultural groups as uniform."},
    {"id": "com-001", "topic_id": "complementary-treatment", "difficulty": "Applied", "prompt": "A person wants to add a complementary practice to evidence-based treatment. What is the most appropriate first step?", "choices": ["Stop their existing treatment immediately", "Discuss safety, potential interactions and available evidence with a qualified professional", "Assume natural means risk-free", "Trust promotional testimonials over safety information"], "correct_index": 1, "explanation": "Complementary approaches should be evaluated for evidence, safety and interactions. They do not automatically replace established care."},
    {"id": "com-002", "topic_id": "complementary-treatment", "difficulty": "Critical", "prompt": "A treatment has many positive testimonials but few controlled studies. Which statement is most defensible?", "choices": ["Testimonials establish effectiveness", "All treatments without trials are harmful", "Popularity alone is sufficient proof", "Personal reports are informative but cannot by themselves establish efficacy"], "correct_index": 3, "explanation": "Controlled research helps distinguish treatment effects from expectancy effects, selection bias and natural change."},
    {"id": "afr-001", "topic_id": "african-psychologies", "difficulty": "Conceptual", "prompt": "Why might the plural expression 'African psychologies' be useful in academic debate?", "choices": ["It implies one unchanging African worldview", "It allows for multiple histories, methods and intellectual approaches", "It rejects all empirical research", "It makes all theories equivalent"], "correct_index": 1, "explanation": "The plural form highlights intellectual diversity and avoids representing a continent as a single perspective. This is an illustrative question, not a substitute for Ratele's text."},
    {"id": "afr-002", "topic_id": "african-psychologies", "difficulty": "Critical", "prompt": "What is one danger of importing a psychological theory without examining its original social setting?", "choices": ["It may present context-dependent assumptions as universal", "It guarantees more precise findings", "It eliminates the need for translation", "It ensures theories are equally valid everywhere"], "correct_index": 0, "explanation": "Frameworks developed in particular contexts can contain assumptions that require testing and interpretation in other settings."},
    {"id": "pos-001", "topic_id": "positive-psychology", "difficulty": "Applied", "prompt": "A well-being programme focuses on individual optimism but ignores food insecurity and community support. What is a reasonable critique?", "choices": ["Optimism always makes poverty irrelevant", "Social conditions cannot affect well-being", "An exclusively individual focus can miss relational and structural influences", "Well-being cannot be studied"], "correct_index": 2, "explanation": "Contextual approaches consider relationships, resources and inequalities alongside individual strengths."},
    {"id": "pos-002", "topic_id": "positive-psychology", "difficulty": "Conceptual", "prompt": "Why would a community-centred well-being measure include social connectedness?", "choices": ["All cultures define happiness identically", "Relationships can be part of how well-being is experienced and sustained", "Connectedness is only relevant in childhood", "Questionnaires cannot measure relationships"], "correct_index": 1, "explanation": "Social connections and collective contexts can be central to experiences of well-being; measurement should reflect the construct being studied."},
]
# All original demonstration questions from the first version belong to Medium.
for _question in _BANK:
    _question["mode"] = "medium"
_BANK.extend(NEW_QUESTIONS)
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
    fields = ("id", "topic_id", "prompt", "choices", "difficulty", "mode")
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
    }
