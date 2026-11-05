# The ai folder: a handoff for any AI assistant

This folder is the context an AI assistant (Claude, ChatGPT, Gemini, a local model) needs to pick up work on this site without the original chat history. It was written on 2026-11-04 by the assistant that built the site with Dante, and it is meant to be kept current: whoever works here next appends to `SESSION_LOG.md` and corrects the other files when they change something.

This repository is public (GitHub Pages on a free plan requires it), so nothing private belongs in this folder. Personal matters stay in Dante's private knowledge base, which is described but not reproduced in `RELATED_WORK.md`.

## How to use it

Paste or attach these in this order, as far as the model's context allows:

1. `HANDOFF.md`: who Dante is, what the site is, where it stands, what to do next. Enough on its own for content work.
2. `STYLE_AND_FEEDBACK.md`: how Dante wants writing and layout done, learned from direct feedback. Read before writing any text or changing any layout.
3. `SITE_INTERNALS.md`: how `build.py`, `studio.py`, the templates and the CSS work. Needed before touching code.
4. `CONTENT_STATUS.md`: every project, what it has, what it is missing.
5. `DECISIONS.md`: why things are the way they are, and what was tried and rejected, so it is not re-proposed.
6. `RELATED_WORK.md`: Dante's other folders and tools that this site connects to.
7. `SESSION_LOG.md`: dated record of what was done.

A short opening prompt that works:

> Read ai/HANDOFF.md, ai/STYLE_AND_FEEDBACK.md and ai/SITE_INTERNALS.md in this repo before doing anything. Then: (what you want done today).

## Keeping it current

- When you change how the build, studio or layout works, update `SITE_INTERNALS.md`.
- When a project gets its photos or its real write-up, update `CONTENT_STATUS.md`.
- When Dante gives feedback on tone or design, add it to `STYLE_AND_FEEDBACK.md` with the date.
- End every working session with a dated entry in `SESSION_LOG.md`.
