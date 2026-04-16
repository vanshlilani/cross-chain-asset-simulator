import requests
from time import sleep

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

ASSET_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana"
}


def get_crypto_price(symbol):
    if symbol not in ASSET_MAP:
        return None, "Unsupported asset"

    coin_id = ASSET_MAP[symbol]

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(
                COINGECKO_URL,
                params={"ids": coin_id, "vs_currencies": "usd"},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                price = data[coin_id]["usd"]
                return price, None

        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                sleep(1)
            else:
                return None, "External API failed"

    return None, "Unknown error"