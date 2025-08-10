# Changelog

All notable changes to this project will be documented in this file.

## [3.0.1] - 2025-08-10
### Fixed
- Frontend assets now correctly served under `/assets` from FastAPI; fixed SPA catch-all to avoid intercepting static files.
- Production start scripts aligned; verified health and contacts stats endpoints via ngrok.

### Added
- Documentation updates to describe static serving and verification steps.
- Release checklist and GitHub preparation guide.

### Changed
- Root `.gitignore` hardened to exclude venvs, node_modules, dist, and databases.

## [3.0.0] - 2025-08-07
### Added
- LLM enabled by default (Qwen via DashScope).
- Telegram bot integrated to backend agent flow.
- Contacts normalization & deduplication across create/update/import flows.
