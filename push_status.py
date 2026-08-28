"""Pushes this desktop's live master-agent status out to a deployed FRIDAY
instance every ~20s, so FRIDAY can be hosted somewhere public and still show
real data. Read-only against master-agent -- only ever GETs its public
/api/status endpoint, exactly like a browser tab would. Never touches any
agent's files or processes.

Config comes from this same folder's .env:
  FRIDAY_INGEST_KEY   shared secret -- must match the deployed host's env var
  FRIDAY_PUBLIC_URL   e.g. https://friday-xxxx.onrender.com (no trailing slash)

Run:  python push_status.py
"""

import json
import os
import time
import urllib.request
from urllib.error import URLError

import requests

MASTER_AGENT_STATUS_URL = "http://127.0.0.1:9000/api/status"
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
PUSH_INTERVAL_SECONDS = 20


def read_env(var_name):
    if not os.path.isfile(ENV_PATH):
        return None
    with open(ENV_PATH, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            if key.strip() == var_name and val.strip():
                return val.strip()
    return None


def fetch_local_status():
    with urllib.request.urlopen(MASTER_AGENT_STATUS_URL, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def push_once(public_url, ingest_key):
    data = fetch_local_status()
    resp = requests.post(
        f"{public_url}/ingest",
        headers={"X-Ingest-Key": ingest_key, "Content-Type": "application/json"},
        json=data,
        timeout=10,
    )
    resp.raise_for_status()
    return data["summary"]["total_agents"]


def main():
    public_url = (read_env("FRIDAY_PUBLIC_URL") or "").rstrip("/")
    ingest_key = read_env("FRIDAY_INGEST_KEY")

    if not public_url:
        print("FRIDAY_PUBLIC_URL is empty in .env -- fill it in once FRIDAY is deployed, then restart this.")
        return
    if not ingest_key:
        print("FRIDAY_INGEST_KEY is empty in .env -- this should already be set; check the file.")
        return

    print(f"Pushing http://127.0.0.1:9000 status -> {public_url}/ingest every {PUSH_INTERVAL_SECONDS}s")
    while True:
        try:
            n = push_once(public_url, ingest_key)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] pushed {n} agents OK")
        except (URLError, OSError) as exc:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] master-agent unreachable locally: {exc}")
        except requests.RequestException as exc:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] push to {public_url} failed: {exc}")
        time.sleep(PUSH_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
