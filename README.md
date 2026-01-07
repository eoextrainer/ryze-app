# RYZE Frontend (nested repo)

Nested Git repo scoped to `/media/eoex/DOJO/CONSULTING/PROJECTS/TEST/RYZE` to avoid parent changes.

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Git
- `git remote -v` -> `git@github.com:eoextrainer/ryze-app.git`
- Local config set to `Ryze Bot <bot@ryze.local>` for commits from automation.

## Auto workflow
- Configure env from `.env.example`.
- `python scripts/auto_workflow.py once` or `watch` for continuous.
- Rollback via `python scripts/auto_workflow.py rollback <hash>` (creates revert commit).
- See `AUTO_WORKFLOW.md` for details.

## Database (Postgres)
- `docker compose -f docker-compose.db.yml up -d` to start Postgres + seeds (`db/init/`).
- Tables: `users`, `change_iterations` for audit trail.

## Admin UI
- Admin audit table in `index.html` (visible when logged in as admin via demo login).
- Demo credentials documented in `docs/credentials.md` and seeded in `db/init/seed.sql`.

## Theming & runtime
- 20 visual themes (Netflix/Google Play/Apple-inspired) auto-rotate every 60s based on time of day (brighter mornings, darker nights). Per-user choices persist via localStorage; pick from the theme selector on the login section.

## Serve locally
- `bash scripts/serve.sh` restarts a static server on port 8000, kills any existing process on that port, and opens the browser.
