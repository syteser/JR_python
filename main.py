import requests
import ccxt
import datetime

programm_version='0.0.0.1'
programm_author = '@syteser'
programm_name = ''
# количество часов для выборок
timeframe_hours = 7
# Список основных монет
symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"]

print(f'************************************************')
print(f'HELLO!!!')
print(f'Версія програми - {programm_version}')
print(f'author: {programm_author} 2025')
print(f'************************************************')

import requests
import datetime

def fetch_recent_transactions(timeframe_hours):
    """
    Получает данные о последних транзакциях в блокчейне за заданный промежуток времени.
    :param timeframe_hours: Временной промежуток в часах
    :return: Список транзакций
    """
    base_url = "https://blockchain.info/unconfirmed-transactions?format=json"
    response = requests.get(base_url)
    response.raise_for_status()

    data = response.json()
    transactions = data.get("txs", [])

    now = datetime.datetime.now(datetime.UTC)
    timeframe_start = now - datetime.timedelta(hours=timeframe_hours)
    timeframe_start_ts = int(timeframe_start.timestamp())

    # Фильтруем транзакции по времени
    recent_transactions = [
        tx for tx in transactions if tx.get("time", 0) >= timeframe_start_ts
    ]

    return recent_transactions

def analyze_blockchain_movements(timeframe_hours, threshold_btc):
    """
    Анализирует изменения в блокчейне и ищет транзакции, превышающие указанный порог.

    :param timeframe_hours: Временной промежуток в часах
    :param threshold_btc: Пороговое значение в BTC
    """
    try:
        transactions = fetch_recent_transactions(timeframe_hours)

        for tx in transactions:
            total_input = sum(inp.get("prev_out", {}).get("value", 0) for inp in tx.get("inputs", [])) / 1e8  # Сатоши в BTC
            total_output = sum(out.get("value", 0) for out in tx.get("out", [])) / 1e8

            if total_input >= threshold_btc:
                print(f"Транзакция {tx.get('hash')} потратила {total_input:.8f} BTC.")

            if total_output >= threshold_btc:
                print(f"Транзакция {tx.get('hash')} получила {total_output:.8f} BTC.")

    except Exception as e:
        print(f"Ошибка при анализе блокчейна: {e}")

def analyze_crypto_changes(symbols, timeframe_hours):
    """
    Анализирует изменения цен для заданных монет за указанный промежуток времени.

    :param symbols: Список валютных пар (например, ["BTC/USDT", "ETH/USDT"])
    :param timeframe_hours: Временной промежуток в часах для анализа
    """
    # Подключение к Binance API через ccxt
    exchange = ccxt.binance()
    now = datetime.datetime.now(datetime.UTC)

    print(f"Анализ изменений за последние {timeframe_hours} часов:")

    for symbol in symbols:
        try:
            # Получаем исторические данные OHLCV (цена открытия, высокая, низкая, закрытия, объем)
            since = int((now - datetime.timedelta(hours=timeframe_hours)).timestamp() * 1000)
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1h", since=since)

            if not ohlcv:
                print(f"Нет данных для {symbol}.")
                continue

            # Берем первую и последнюю цену закрытия
            open_price = ohlcv[0][1]  # Цена открытия первой свечи
            close_price = ohlcv[-1][4]  # Цена закрытия последней свечи

            # Вычисляем изменение в процентах
            change_percent = ((close_price - open_price) / open_price) * 100

            # Определяем, выросла или упала монета
            status = "выросла" if change_percent > 0 else "упала"

            print(f"Монета {symbol.split('/')[0]} {status} на {abs(change_percent):.2f}% за последние {timeframe_hours} часов.")

        except Exception as e:
            print(f"Ошибка при обработке {symbol}: {e}")

if __name__ == "__main__":
#    рух Х монет протягом timeframe_hours годин
    analyze_crypto_changes(symbols, timeframe_hours)

    timeframe_hours = 24  # Количество часов
    threshold_btc = 1  # Порог в биткоинах
    analyze_blockchain_movements(timeframe_hours, threshold_btc)
