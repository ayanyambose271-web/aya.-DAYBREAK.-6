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
        assert set(question) == {"id", "topic_id", "prompt", "choices", "difficulty", "mode", "source"}
        assert len(question["choices"]) == 4
        assert "correct_index" not in question
        assert "explanation" not in question


def test_invalid_topic_raises_value_error():
    with pytest.raises(ValueError, match="Unknown topic"):
        get_questions("not-a-topic", 1)


def test_grading_correct_answer():
    result = grade_answer("psyc26-psy-m1", 0)
    assert result["correct"] is True
    assert result["correct_index"] == 0
    assert result["explanation"]


def test_grading_wrong_answer():
    result = grade_answer("psyc26-psy-m1", 1)
    assert result["correct"] is False
    assert result["correct_index"] == 0


def test_bad_question_or_choice_is_rejected():
    with pytest.raises(ValueError, match="Unknown question"):
        grade_answer("none", 0)
    with pytest.raises(ValueError, match="between 0 and 3"):
        grade_answer("psyc26-psy-m1", 5)


def test_medium_and_hard_modes_have_four_unique_questions_per_topic():
    ids = set()
    for topic in TOPICS:
        for mode in ("medium", "hard"):
            questions = get_questions(topic["id"], 4, mode=mode)
            assert len(questions) == 4
            assert all(q["mode"] == mode for q in questions)
            assert len({q["id"] for q in questions}) == 4
            assert not any(q["id"] in ids for q in questions)
            ids.update(q["id"] for q in questions)
    assert len(ids) == 48


def test_invalid_mode_does_not_fallback_to_other_mode():
    with pytest.raises(ValueError, match="Unknown difficulty mode"):
        get_questions("psychopathology", 4, mode="extreme")


def test_hard_questions_require_scenario_reasoning():
    questions = get_questions("psychopathology", 4, mode="hard")
    assert all(len(q["prompt"]) >= 115 for q in questions)
    assert all(len(q["choices"]) == 4 for q in questions)


def test_grading_returns_mode_for_mode_specific_statistics():
    question = get_questions("psychopathology", 1, mode="hard")[0]
    result = grade_answer(question["id"], 0)
    assert result["mode"] == "hard"
