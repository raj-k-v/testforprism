# `demo_bad_pr.py` — What Each Line Is Meant to Trip

Reference guide for `backend/tests/fixtures/intentionally_flawed.py`, a test fixture
built to exercise PRism's review categories end-to-end.

> **DO NOT MERGE** — this file is intentionally broken and exists only to validate
> that the review bot catches real issues.

## Line-by-line breakdown

| Line | Category | What PRism should flag |
| --- | --- | --- |
| `API_KEY = "sk-live-..."` | Security | Hardcoded secret. Also worth confirming `review_service.py`'s redaction step masks it before it's ever posted or stored. |
| `"...WHERE username = '" + username + "'"` | Security | SQL injection via string concatenation instead of parameterized queries. |
| `scores[s] / total` | Bug | Division by zero — no guard against `total == 0`. |
| `open(path)` without `close()` / context manager | Bug / Maintainability | Resource leak — file handle is never closed. |
| Nested loop in `find_duplicates` | Performance | O(n²) complexity where a set-based approach would be O(n). |
| `eval(user_input)` | Security | Arbitrary code execution on untrusted input. |
| `self.discount` magic number, no validation | Maintainability | Unvalidated input (`price` could be negative) and an unexplained constant. |

## How to use this fixture

1. Put `demo_bad_pr.py` on a branch and open a PR against a repo your GitHub App
   is installed on.
2. Confirm `diff_parser.py` maps each finding to an **added** line — this is the
   check that should reject any finding landing on an unrelated line.
3. Cross-check the posted review comments against the table above: every row
   should correspond to at least one finding, and confidence scores below
   `MIN_CONFIDENCE` should be silently dropped rather than posted.
4. If a row doesn't get flagged, that's a gap worth investigating in
   `analyzer.py`'s prompt or `_validate_findings()`'s filtering logic.