# Deploying FRIDAY live (Render, free tier)

This folder is now self-contained enough to deploy on its own. Once it's live,
your desktop keeps it fed via `push_status.py` (see below) -- no admin rights,
no VPN, no tunnel needed anywhere in this.

## 1. Push this folder to GitHub

```bash
cd jarvis-dashboard
git init
git add .
git commit -m "FRIDAY, ready to deploy"
```

Then create a new (can be private) repo on github.com and push to it:

```bash
git remote add origin https://github.com/<you>/friday-dashboard.git
git branch -M main
git push -u origin main
```

## 2. Create the Render service

1. Sign up / log in at [render.com](https://render.com) (free)
2. New -> Web Service -> connect the GitHub repo you just pushed
3. Render should auto-detect: Build command `pip install -r requirements.txt`,
   Start command `python app.py` (from the Procfile)
4. Under **Environment**, add these variables:
   - `FRIDAY_INGEST_KEY` -- copy the value from this folder's `.env`
     (the `FRIDAY_INGEST_KEY=...` line)
   - `GROQ_API_KEY` -- copy from this folder's `.env`, so the chat co-pilot
     keeps working once deployed (optional -- skip if you don't need chat there)
5. Click **Deploy**. Render gives you a URL like `https://friday-xxxx.onrender.com`

## 3. Point the desktop pusher at it

Open this folder's `.env` and set:
```
FRIDAY_PUBLIC_URL=https://friday-xxxx.onrender.com
```
(the exact URL Render gave you, no trailing slash)

Then run, or ask me to set it up to run in the background permanently:
```bash
python push_status.py
```

Within ~20 seconds the deployed URL will start showing real data, with a
"SYNCED FROM DESKTOP -- LAST PUSH Ns AGO" badge instead of the local one.
If the desktop is off or push_status.py isn't running, the page keeps
showing the last snapshot it received rather than going blank.

## Notes

- Free Render web services sleep after 15 minutes of no traffic and take
  ~30-60s to wake on the next visit -- fine for occasional checking, less
  fine if you want it always instant. Render's paid tier removes the sleep.
- Nothing about master-agent or any other agent changes -- this only adds
  an outbound push from the desktop and a cache to receive it.
