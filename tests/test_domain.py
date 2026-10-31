import pytest
from daybreak import TOPICS, get_questions, grade_answer


def test_six_distinct_topics():
    assert len(TOPICS) == 6
    assert len({topic["id"] for topic in TOPICS}) == 6


def test_questions_are_public_safe_and_have_unique_ids():
    questions = get_questions("psychopathology", 2)
    assert len(questions) == 2
    assert len({q["id"] for q in questions}) == 2
    for question in questions:
        assert set(question) == {"id", "topic_id", "prompt", "choices", "difficulty"}
        assert len(question["choices"]) == 4
        assert "correct_index" not in question
        assert "explanation" not in question


def test_invalid_topic_raises_value_error():
    with pytest.raises(ValueError, match="Unknown topic"):
        get_questions("not-a-topic", 1)


def test_grading_correct_answer():
    result = grade_answer("psy-001", 1)
    assert result["correct"] is True
    assert result["correct_index"] == 1
    assert result["explanation"]


def test_grading_wrong_answer():
    result = grade_answer("psy-001", 0)
    assert result["correct"] is False
    assert result["correct_index"] == 1


def test_bad_question_or_choice_is_rejected():
    with pytest.raises(ValueError, match="Unknown question"):
        grade_answer("none", 0)
    with pytest.raises(ValueError, match="between 0 and 3"):
        grade_answer("psy-001", 5)
