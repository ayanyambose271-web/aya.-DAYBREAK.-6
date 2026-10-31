# DAYBREAK Study Lab — working demonstration

A small complete browser app with a **FastAPI Python backend**, responsive HTML/CSS/JS frontend, question grading, locally stored practice history, automated Python tests, GitHub Actions CI, and a Vercel-compatible deployment entrypoint.

**Important:** Contains 12 original **sample** questions. It is **not** a course-sourced exam guide; replace the bank with rigorously checked materials before treating it as authoritative.

## Run locally

Requirements: Python 3.13 (3.12+ likely works).

```bash
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m uvicorn app:app --reload
```

Open <http://127.0.0.1:8000>. Swagger API docs: <http://127.0.0.1:8000/api/docs>.

## API

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Web interface |
| `GET /api/health` | Health check |
| `GET /api/topics` | List topics |
| `GET /api/questions?topic_id=psychopathology&count=2` | Questions (answer key omitted) |
| `POST /api/grade` | Grade `{ "question_id": "psy-001", "answer_index": 1 }` and return explanation |

## The four-tool workflow

1. **Superpowers:** Agree on scope, write an implementation plan, create failing tests first (TDD), implement and verify.
2. **Python:** FastAPI serves a browser UI and question APIs; `pytest` tests logic and HTTP routes.
3. **GitHub:** Create a repository, commit these files and open a pull request. `.github/workflows/tests.yml` runs tests on pushes and PRs. Protect `main` so changes require passing checks before merging.
4. **Vercel:** Import the GitHub repo through the Vercel dashboard, choose **FastAPI** or the automatically detected framework, and deploy a preview first. The entrypoint is the root-level `app.py` with a variable named `app`, as supported by Vercel. Verify `/`, `/api/health`, the static assets and the quiz interaction on preview before production.

Vercel's Python runtime supports FastAPI (see https://vercel.com/docs/frameworks/backend/fastapi). A connected Git repo can automatically deploy new commits and PR previews. Confirm project/team ownership and the intended branch before deploying.

## Files

- `app.py`: FastAPI route handlers and site entrypoint
- `daybreak.py`: sample topic and question data, grading engine
- `static/index.html`: accessible app structure
- `static/styles.css`: responsive dark UI
- `static/app.js`: browser interaction and local progress
- `tests/`: domain and API regression tests
- `.github/workflows/tests.yml`: GitHub CI tests

## Security and architecture notes

- Question answers are not included in `GET /api/questions`; the server checks submissions.
- The question bank is *in the source code*, and anyone with access to the source can read it; use this only as a learning prototype, not a secure high-stakes testing product.
- Progress is stored only in this browser's `localStorage`; it is not synced between devices and can be wiped by clearing browser storage.
- No login, database, AI generation, file uploads, payments, usage tracking or background agents are installed.
- Avoid adding secret API keys to the repository. Use Vercel project environment variables for later integrations.
- Test coverage here checks Python logic and API responses; browser click-through testing on an actual Vercel preview would be a separate release gate.
