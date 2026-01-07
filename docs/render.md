# Deploying RYZE to Render (frontend, backend, and Postgres)

These steps describe a full Render blueprint: Postgres database, optional backend API, and the static frontend in this repo.

## Prerequisites
- Render account with GitHub connected.
- Repo pushed (e.g., `git@github.com:eoextrainer/ryze-app.git`) with `render.yaml` in root.
- Backend code ready (if you plan to run an API). This repo currently ships only the static frontend; wire your API repo/path before enabling the backend block.

## One-time setup
1) Push latest code to the branch you want to deploy (e.g., `main`).
2) Open Render → New + → `Blueprint` (YAML) or `Static Site`.
3) If using Blueprint:
   - Point to your GitHub repo.
   - Keep branch to deploy (e.g., `main`).
   - Confirm auto-deploy on push is enabled.
4) If using Static Site instead:
   - Name: `ryze-app` (or your choice).
   - Build command: leave empty (static, no build).
   - Publish directory: `.` (root with `index.html`).
   - Environment: `Static Site`.

## Render configuration (render.yaml)
- Declares:
  - `ryze-db` Postgres (free plan by default).
  - `ryze-app-static` static site publishing the repo root (`.`) with no build step.
  - An optional `ryze-api` web service block (commented). Point it to your backend when ready and uncomment.
- Static site sets `API_BASE_URL` env var placeholder—populate with your backend URL after it’s live.
- HTTP caching headers are set for basic assets; adjust as needed.

## Deploy
1) In Render, click **Blueprint** → select this repo/branch → **Apply**.
   - If only front-end: leave backend block commented; the static site will deploy.
   - If API ready: uncomment `ryze-api`, adjust `buildCommand`/`startCommand`, and redeploy.
2) Wait for initial deploy(s) to finish; verify:
   - Frontend URL: e.g., `https://ryze-app-static.onrender.com`
   - Backend URL: e.g., `https://ryze-api.onrender.com` (if enabled)
3) Enable auto-deploy on push so future commits redeploy automatically.
4) For the frontend, set `API_BASE_URL` to the backend URL (Render → ryze-app-static → Environment).

## Custom domain (optional)
1) In the service settings, add your domain.
2) Create the DNS records Render shows (CNAME for subdomains; A/ALIAS for apex).
3) Wait for SSL provisioning to complete (typically a few minutes).

## Rollbacks
- Render keeps previous deploys per service. In the service → Deploys tab, pick a prior deploy and click **Rollback** (frontend and backend independently).
- This mirrors the git revision deployed at that time.

## Environment & logging
- Static site: optional `API_BASE_URL`.
- Backend (if enabled): set `DATABASE_URL` from the Render Postgres connection string, plus any secrets needed (JWT keys, etc.).
- Logs: view per service (Events/Logs tabs). Postgres logs are available in the database service view.

## Ongoing changes
- Commit and push to the tracked branch; Render auto-redeploys.
- To pause deploys, disable Auto Deploy from service settings; re-enable when ready.
