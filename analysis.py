import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def fetch_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=1"
    response = requests.get(url).json()
    prices = response.get("prices", [])
    if not prices or len(prices) < 3:
        return None
    current_price = prices[-1][1]
    previous_price = prices[-2][1]
    price_30min_ago = prices[-4][1] if len(prices) >= 4 else previous_price
    return current_price, previous_price, price_30min_ago

def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def analyze_market(coins):
    for coin in coins:
        data = fetch_data(coin)
        if not data:
            continue

        current_price, previous_price, price_30min_ago = data
        price_change = current_price - previous_price
        price_slope = current_price - price_30min_ago

        signal_strength = 0
        direction = "neutro"
        indicators = []

        if price_change > 0 and price_slope > 0:
            signal_strength += 2
            direction = "alta"
            indicators.append("ð TendÃªncia de alta")
        elif price_change < 0 and price_slope < 0:
            signal_strength += 2
            direction = "baixa"
            indicators.append("ð TendÃªncia de baixa")

        if abs(price_change / previous_price) > 0.015:
            signal_strength += 1
            indicators.append("ð¥ Movimento forte detectado")

        if direction == "alta" and signal_strength >= 3:
            target = round(current_price * 1.03, 4)
            message = (
                f"ð¢ COMPRA AGORA: {coin.upper()} em zona de entrada segura
"
                f"ð¯ Alvo estimado: ${target}

"
                f"PreÃ§o atual: ${current_price:.4f}
" + "
".join(indicators)
            )
            send_alert(message)

        elif direction == "baixa" and signal_strength >= 3:
            target = round(current_price * 0.97, 4)
            message = (
                f"â ï¸ VENDE JÃ: {coin.upper()} em zona de sobrecompra
"
                f"ð¯ Alvo estimado de queda: ${target}

"
                f"PreÃ§o atual: ${current_price:.4f}
" + "
".join(indicators)
            )
            send_alert(message)
