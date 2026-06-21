from __future__ import annotations

import os
from pathlib import Path

from openrouter import OpenRouter

MODEL = "openrouter/freemodel"


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


def get_optional_env(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def maybe_run_chat_test(client: OpenRouter) -> None:
    if os.getenv("OPENROUTER_RUN_CHAT") != "1":
        return
    response = client.chat.send(
        model=MODEL,
        messages=[{"role": "user", "content": "Hello from the API keys example."}],
    )
    print(response.choices[0].message.content)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    load_env_file(repo_root / ".env")

    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise SystemExit("Missing OPENROUTER_API_KEY in .env or environment")

    key_hash = os.getenv("OPENROUTER_KEY_HASH", "")
    if not key_hash:
        raise SystemExit("Missing OPENROUTER_KEY_HASH in .env or environment")

    with OpenRouter(
        api_key=api_key,
        http_referer=get_optional_env("OPENROUTER_SITE_URL"),
        x_open_router_title=get_optional_env("OPENROUTER_SITE_NAME"),
        x_open_router_categories=get_optional_env("OPENROUTER_CATEGORIES"),
    ) as client:
        res = client.api_keys.delete(hash=key_hash)
        print(res)
        maybe_run_chat_test(client)


if __name__ == "__main__":
    main()
