# DAYBREAK Study Lab — PSY144 2026 source-grounded edition

Browser-based medium/hard MCQ practice for Stellenbosch University PSY144. Built with FastAPI, Python, JavaScript, pytest and deployable to Vercel.

## What is in v0.3

- **48 original questions:** 4 Medium + 4 Hard per topic, across six named Term 3/4 revision topics.
- Answer explanations reveal the supporting reading or slide deck **after** the attempt.
- Source tags distinguish **prescribed textbook evidence** from **2026 lecture evidence**.
- Separate local browser progress tracking for Medium and Hard.
- No user accounts, personal information, uploaded copyrighted PDFs, or source textbook passages embedded in this public repository.

## Evidence coverage

**Directly checked against uploaded textbook:**
- Swartz et al. (2021), *Psychology: An Introduction*, fifth edition, Chapter 24 (Cartwright), PDF pp. 1250–1254: defining psychopathology.
- Swartz et al. (2021), Chapter 18 (Terre Blanche & Stevens), PDF pp. 934–938: poverty, social context and inequality.

**Directly checked against the user's 2026 lecture presentations (not against the unprovided full prescribed texts):**
- `Poverty 2026 upload copy.pptx`; `Ethnicity 2026 upload copy.pptx`.
- `Culture and Mental health 2026 1.pptx`; `Culture and Mental Health Psyc 144 2026 week 2 upload copy.pptx`.
- `African Psy, Lecture 1 of 2, 2026.pptx`; `African Psy, Lecture 2 of 2, 2026.pptx` (Ratele orientations).
- `African Psy, WellBeing in Africa African Pos Psy, Lectures 1 of 2, 2026.pptx` and `Lectures 2 of 2` (Fadiji, Khumalo & Zulu overview).

**Limits:** Weiten & Ntozini (2022) Chapters 16–17 and the full Ratele (2017) / Fadiji et al. (2022) texts have not been directly checked. These topics must display **LECTURE GROUNDED**, not textbook verified. The six-topic revision bank is not the complete course examination blueprint; developmental and personality topics may also be examinable. The questions are our own, not actual SU examination material.

## Local development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` and API documentation at `/api/docs`.

## API

- `GET /api/health`
- `GET /api/topics`
- `GET /api/sources` — source register and limits
- `GET /api/questions?topic_id=psychopathology&mode=hard&count=4`
- `POST /api/grade` with `{"question_id":"psyc26-psy-m1","answer_index":0}`

Question responses never reveal answer keys; the grade route returns the correct answer, explanation and source. This is a practice application, not a secured examination system (a motivated user can inspect application source).
