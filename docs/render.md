# Deploying RYZE to Render (static site)

These steps publish the current static build (root `index.html`) on Render. Adjust names as needed for your account.

## Prerequisites
- Render account with GitHub connected.
- Repo pushed (e.g., `git@github.com:eoextrainer/ryze-app.git`) with `render.yaml` in root.

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
- The provided `render.yaml` in repo declares a static site named `ryze-app-static`.
- It publishes the repository root (`.`) and skips a build command for speed.
- HTTP caching headers are set for basic assets; adjust as needed.

## Deploy
1) In Render, click **Create Static Site** (or **Apply** for Blueprint).
2) Wait for initial deploy to finish; verify the Render URL (e.g., `https://ryze-app-static.onrender.com`).
3) Enable auto-deploy on push so future commits redeploy automatically.

## Custom domain (optional)
1) In the service settings, add your domain.
2) Create the DNS records Render shows (CNAME for subdomains; A/ALIAS for apex).
3) Wait for SSL provisioning to complete (typically a few minutes).

## Rollbacks
- Render keeps previous deploys. In the service → Deploys tab, pick a prior deploy and click **Rollback**.
- This mirrors the git revision deployed at that time.

## Environment & logging
- No env vars needed for the static site.
- Logs are minimal (static hosting); status is visible in the service Events tab.

## Ongoing changes
- Commit and push to the tracked branch; Render auto-redeploys.
- To pause deploys, disable Auto Deploy from service settings; re-enable when ready.
