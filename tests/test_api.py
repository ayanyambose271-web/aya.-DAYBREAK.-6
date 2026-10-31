from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "DAYBREAK" in response.text
    assert "text/html" in response.headers["content-type"]


def test_topics():
    response = client.get("/api/topics")
    assert response.status_code == 200
    assert len(response.json()["topics"]) == 6


def test_questions_obscure_answer_key():
    response = client.get("/api/questions", params={"topic_id": "psychopathology", "count": 2})
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 2
    for question in response.json()["questions"]:
        assert "correct_index" not in question
        assert "explanation" not in question


def test_invalid_topic_returns_404():
    assert client.get("/api/questions", params={"topic_id": "missing"}).status_code == 404


def test_count_is_validated():
    assert client.get("/api/questions", params={"topic_id": "psychopathology", "count": 0}).status_code == 422


def test_grade_answer_through_api():
    response = client.post("/api/grade", json={"question_id": "psyc26-psy-m1", "answer_index": 0})
    assert response.status_code == 200
    assert response.json()["correct"] is True
    assert response.json()["source"]["basis"] == "prescribed_textbook"


def test_bad_question_through_api():
    response = client.post("/api/grade", json={"question_id": "bad", "answer_index": 1})
    assert response.status_code == 404


def test_static_asset_is_served():
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "async function beginTopic" in response.text


def test_hard_mode_api_only_returns_hard_questions():
    response = client.get("/api/questions", params={"topic_id": "psychopathology", "count": 4, "mode": "hard"})
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 4
    assert all(q["mode"] == "hard" for q in response.json()["questions"])
    assert all("correct_index" not in q for q in response.json()["questions"])


def test_unknown_mode_rejected_by_api():
    response = client.get("/api/questions", params={"topic_id": "psychopathology", "mode": "extreme"})
    assert response.status_code == 422


def test_medium_mode_default_and_ui_selectors_exist():
    response = client.get("/api/questions", params={"topic_id": "psychopathology", "count": 4})
    assert response.status_code == 200
    assert all(q["mode"] == "medium" for q in response.json()["questions"])
    html = client.get("/").text
    assert 'id="mode-select"' in html
    assert 'data-mode="hard"' in html
    assert 'data-mode="medium"' in html


def test_course_source_register_is_exposed_without_full_copyrighted_text():
    response = client.get("/api/sources")
    assert response.status_code == 200
    assert response.json()["sources"]["T18a"]["basis"] == "prescribed_textbook"
    assert response.json()["sources"]["W2"]["basis"] == "course_lecture"

def test_page_explains_lecture_vs_textbook_evidence():
    page = client.get("/").text
    assert "Textbook-verified" in page
    assert "Lecture-grounded" in page
    assert "not official exam items" in page
