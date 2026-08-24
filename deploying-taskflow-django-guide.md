# Deploying TaskFlow (Django + HTMX) to Render

A step-by-step guide to taking the TaskFlow Django demo from a local
project to a live, publicly accessible website — using Render to host
both the Django application and a managed PostgreSQL database in one
dashboard.

**Order matters.** Set these up database → web service, in that order —
the web service step needs a real connection string produced by the
database step.

---

## Prerequisites

- The `task-flow-django` project pushed to a GitHub repository (see
  `gitignore-env-secrets-guide.md` for safely getting it there without
  committing any secrets)
- A free account on [Render](https://render.com)

---

## Step 1: Create the database on Render

1. In Render: **New → PostgreSQL**.
2. Give it a name (e.g. `task-flow-db`), choose the free or Starter
   tier, and create it.
3. Once provisioned, open the database's page and copy the **Internal
   Database URL** (not the external one — the internal URL is faster
   and free, since traffic between two Render services in the same
   account stays on Render's private network). It looks like:
   ```
   postgresql://<user>:<password>@<host>/<database>
   ```
4. Keep this string handy — it's your `DATABASE_URL`, and it's a secret.
   Never commit it to your repo; it only ever goes into the web
   service's environment variable settings (Step 2).

---

## Step 2: Deploy the web service

1. In Render: **New → Web Service** → connect your GitHub repo.
   When prompted for repository access, choose **"Only select
   repositories"** and pick just `task-flow-django` — never grant a
   platform access to every repo in your account.
2. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn task_flow_project.wsgi`
   - **Instance Type**: Starter ($7/month, always-on — the free tier
     spins down after 15 minutes of inactivity, which is fine for
     testing but not for a real user-facing site)
3. Under **Environment Variables**, add:
   - `DATABASE_URL` = the Internal Database URL from Step 1
   - `SECRET_KEY` = a real generated value — never reuse the demo's
     placeholder. Generate one locally with:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(50))"
     ```
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = the Render URL you'll be given, e.g.
     `task-flow-django.onrender.com` (add your custom domain here too,
     once you set one up in Step 4)
4. Deploy. Render gives you a URL like:
   ```
   https://task-flow-django.onrender.com
   ```

---

## Step 3: Apply migrations

The `tasks` table needs to be created on the live database before the
app can use it. Render's **Shell** tab (on your web service's dashboard)
lets you run one-off commands against the live environment:

```bash
python manage.py migrate
```

Run this once after the first successful deploy, and again any time you
add a new migration locally and push it.

---

## Step 4: Verify

Visit your Render URL. You should see the TaskFlow page load, and adding
a task via the form should persist and reappear (confirming HTMX, the
view, and the database are all working end to end).

| Symptom | Likely cause |
|---|---|
| "DisallowedHost" error | Your Render URL (or custom domain) isn't listed in `ALLOWED_HOSTS` — update the environment variable and redeploy |
| 500 error referencing the database | `DATABASE_URL` missing, incorrect, or migrations not yet applied — re-check Step 1 and re-run Step 3 |
| Page loads but form submission does nothing | Check the browser console for a blocked request — confirm the HTMX script tag in `task_list.html` loaded successfully |

---

## Step 5: Connect a custom domain (optional)

In Render: your web service → **Settings → Custom Domains** → add your
domain. Render shows the exact DNS records to add at your domain
registrar — remove any leftover AAAA records first, since Render is
IPv4-only and stray AAAA records can interfere with routing and
certificate issuance. Once DNS verifies, Render automatically issues a
free SSL certificate.

---

## Quick reference: what goes where

| Value | Produced by | Used in |
|---|---|---|
| `DATABASE_URL` | Render PostgreSQL's Internal Database URL | Web service environment variable |
| `SECRET_KEY` | Generated locally, once | Web service environment variable |
| `ALLOWED_HOSTS` | Render's assigned URL (or your custom domain) | Web service environment variable |

---

## Appendix: common Git/GitHub errors along the way

These aren't specific to this deployment, but reliably come up for
students pushing a project to GitHub for the first time.

**`fatal: Authentication failed`** — GitHub no longer accepts your
password for Git operations. Use a Personal Access Token, or switch to
SSH authentication.

**`Permission denied (publickey)`** — usually means one of:
- Your SSH key was never loaded into your SSH agent — run
  `ssh-add ~/.ssh/id_ed25519` (start the agent first with
  `eval "$(ssh-agent -s)"` if you see "Could not open a connection to
  your authentication agent").
- The public key on your machine doesn't match what's uploaded to
  GitHub — compare `cat ~/.ssh/id_ed25519.pub` against
  **GitHub → Settings → SSH and GPG keys**.

**`gpg: signing failed: Unusable secret key`** — your Git config is
pointed at a GPG key that no longer exists (e.g. after regenerating your
keys). Either update Git to your new key ID
(`git config --global user.signingkey <new-key-id>`), or disable commit
signing entirely for a student/portfolio project:
```bash
git config --global commit.gpgsign false
```

**`fatal: Could not read from remote repository`** — almost always
means the repository doesn't exist yet at that exact URL. Create it on
GitHub first (without initializing a README/`.gitignore`, since your
local project already has content), then push again.

**Before every push**, run `git status` and confirm `.env` never
appears in the list of files about to be committed — see
`gitignore-env-secrets-guide.md` for the full reasoning and a one-time
history check (`git log --all --full-history -- "**/.env"`) if you're
verifying an existing repo.
