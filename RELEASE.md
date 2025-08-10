# Release Guide

This document describes how to prepare and publish a new functional release of scAIe CRM to GitHub.

## 1) Pre-flight checks
- Backend health: `GET /health` returns `{ "status": "healthy" }`.
- Frontend assets: `GET /assets/index.css` and `GET /assets/index.js` return 200.
- Admin UI: `/contacts` loads with styles and data.
- Key endpoints:
  - `GET /api/contacts?skip=0&limit=5` works
  - `GET /api/contacts/stats` works

## 2) Versioning
- Bump version in root `README.md`.
- Add a new entry in `CHANGELOG.md`.

## 3) Git hygiene
- Ensure `.gitignore` excludes: venv, node_modules, dist, logs, and .db files.
- Avoid committing credentials: `.env` and related files are ignored.

## 4) Commit and tag
- Commit changes with a conventional message, e.g.:
  - `chore(release): 3.0.1 – serve SPA assets from FastAPI, docs & ignore updates`
- Tag the release: `git tag -a v3.0.1 -m "3.0.1: SPA assets fix, docs"`
- Push: `git push origin main --tags`

## 5) GitHub Release
- Create a GitHub Release `v3.0.1`.
- Paste highlights from `CHANGELOG.md`.

## 6) Post-release
- Validate public URL (ngrok if applicable) still serves assets and API.
- Monitor logs for errors: `scaie_crm/logs/*.log`.
