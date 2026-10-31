"""Source coverage and evidence transparency checks for the 2026 PSY144 module."""
from collections import Counter
from daybreak import TOPICS, _BANK, get_questions, grade_answer


def test_four_verified_questions_per_mode_and_topic():
    assert len(_BANK) == 48
    counts = Counter((q['topic_id'], q['mode']) for q in _BANK)
    for topic in TOPICS:
        assert counts[(topic['id'], 'medium')] == 4
        assert counts[(topic['id'], 'hard')] == 4


def test_every_item_has_specific_evidence_not_unsourced_claims():
    for q in _BANK:
        source = q['source']
        assert source['title']
        assert source['location']
        assert source['basis'] in ('prescribed_textbook', 'course_lecture')
        assert 'source' in grade_answer(q['id'], q['correct_index'])
        assert len(q['choices']) == 4 and len(set(q['choices'])) == 4
        assert q['prompt'].endswith('?')


def test_missing_full_readings_are_not_claimed_as_textbook_verified():
    for q in _BANK:
        if q['topic_id'] in ('culture-mental-health', 'complementary-treatment', 'african-psychologies', 'positive-psychology'):
            assert q['source']['basis'] == 'course_lecture'


def test_question_api_never_leaks_answer_key():
    for topic in TOPICS:
        for mode in ('medium', 'hard'):
            for q in get_questions(topic['id'], 4, mode=mode):
                assert 'correct_index' not in q
                assert 'explanation' not in q
                assert q['source']['location']


def test_no_legacy_sample_questions_in_active_bank():
    assert all(q['id'].startswith('psyc26-') for q in _BANK)
