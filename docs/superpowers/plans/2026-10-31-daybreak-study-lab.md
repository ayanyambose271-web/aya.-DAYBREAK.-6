# DAYBREAK Study Lab — demonstration implementation plan

**Purpose:** Demonstrate how Superpowers, Python, GitHub and Vercel work together for a complete, small browser app.

## Design choices
- Frontend: plain HTML, CSS and vanilla JS (minimal dependencies).
- Backend: Python FastAPI, root-level `app.py` for Vercel detection.
- Persistence: browser localStorage only (no external backend resources or secrets).
- Content: 12 original demonstration MCQs over six topic categories; not a course-sourced guide.
- Test-first: Python pytest tests for grading, API shape, validation and static page response.

## Implementation units and acceptance checks
1. `daybreak.py`: topic data, filtered questions, secure-enough answer key handling for a learning demo, grader. Unit tests check answer data is not disclosed by question endpoint, correctness and invalid input.
2. `app.py`: routes for page, health, topics, questions and grading. FastAPI TestClient checks success and failure cases.
3. `static/*`: mobile-responsive page and local progress display. JS syntax check, page and static file retrieval tests.
4. `.github/workflows/tests.yml`: CI pipeline executing tests on pushes and PRs.
5. Vercel: deploy from connected Git repo only when specifically requested and the target project/team is confirmed; then test preview and production.

## Known limitations
- No authenticated users or persistent database.
- Browser-level click testing needs an actual browser runtime; Python tests do not cover all UI interactions.
- Sample questions are not sourced from uploaded course readings.
- Public deployment is a separate user-approved action.
