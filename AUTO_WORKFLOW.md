# RYZE Auto Commit / Push / Rollback workflow

This repo is nested under a larger workspace. All automation is scoped to `./` only.

## Setup
1) Create and activate venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2) Start Postgres for audit logging (optional but recommended):
```bash
docker compose -f docker-compose.db.yml up -d
```
This seeds tables via `db/init/`.
3) Export env (copy `.env.example` to `.env` if desired):
```bash
export DATABASE_URL=postgresql://ryze:ryze@localhost:5432/ryze_changes
export AUTO_PUSH=true
export AUTO_COMMIT_BRANCH=main
export AUTO_COMMIT_PREFIX=auto
```

## Usage
- One-off cycle (add/commit/push/log):
```bash
python scripts/auto_workflow.py once
```
- Continuous watch + auto-commit on file changes:
```bash
python scripts/auto_workflow.py watch
```
- Rollback (creates revert commit and logs):
```bash
python scripts/auto_workflow.py rollback <commit_hash>
```

## Notes
- The watcher ignores `.git`, `.venv`, and temp files.
- DB logging is skipped if `DATABASE_URL` or `psycopg2` is missing.
- Remote is set to `git@github.com:eoextrainer/ryze-app.git`; ensure SSH keys are configured before pushing.
- To align with “change via prompt” requests, trigger `once` after Codex/Copilot changes if the watcher is not running.
