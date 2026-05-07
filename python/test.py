import json
import os
from pathlib import Path

import requests


def load_env_file(env_path: Path) -> None:
  if not env_path.exists():
    return
  for raw_line in env_path.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line:
      continue
    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    if key and key not in os.environ:
      os.environ[key] = value


load_env_file(Path(".env"))

api_key = os.getenv("OPENROUTER_API_KEY")
site_url = os.getenv("OPENROUTER_SITE_URL", "")
site_name = os.getenv("OPENROUTER_SITE_NAME", "")

if not api_key:
  raise SystemExit("Missing OPENROUTER_API_KEY in .env or environment")

headers = {
  "Authorization": f"Bearer {api_key}",
}
if site_url:
  headers["HTTP-Referer"] = site_url
if site_name:
  headers["X-OpenRouter-Title"] = site_name

payload = {
  "model": "openai/gpt-5.2",
  "messages": [
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
}

try:
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps(payload),
    timeout=30,
  )
  response.raise_for_status()
  try:
    print(json.dumps(response.json(), indent=2))
  except json.JSONDecodeError as exc:
    raise SystemExit(f"Invalid JSON response: {exc}") from exc
except requests.exceptions.RequestException as exc:
  raise SystemExit(f"Request failed: {exc}") from exc
