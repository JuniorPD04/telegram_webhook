import os

import requests
from dotenv import load_dotenv


load_dotenv()


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta configurar {name}.")
    return value


def main() -> None:
    token = required_env("TELEGRAM_BOT_TOKEN")
    public_base_url = required_env("PUBLIC_BASE_URL").rstrip("/")
    secret_token = required_env("TELEGRAM_WEBHOOK_SECRET")
    webhook_url = f"{public_base_url}/telegram/webhook"

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/setWebhook",
            json={"url": webhook_url, "secret_token": secret_token},
            timeout=20,
        )
    except requests.RequestException:
        raise RuntimeError("No se pudo conectar con Telegram.") from None
    if not response.ok:
        raise RuntimeError(
            f"Telegram devolvió HTTP {response.status_code} al configurar el webhook."
        )

    result = response.json()
    if not result.get("ok"):
        raise RuntimeError("Telegram no pudo configurar el webhook.")

    print(f"Webhook configurado correctamente en {webhook_url}")


if __name__ == "__main__":
    main()
