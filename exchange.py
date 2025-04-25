import httpx
import logging

logger = logging.getLogger(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/{base}"


async def get_exchange_rate(base: str, target: str) -> float | None:
    url = API_URL.format(base=base)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            rates = response.json().get("rates", {})
            return rates.get(target)
    except Exception as e:
        logger.error(f"[Exchange API] Error while fetching rate for {base} → {target}: {e}")
        return None


def convert_currency(amount: float, rate: float) -> float:
    return round(amount * rate, 2)