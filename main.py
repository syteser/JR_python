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

def fetch_large_transactions(threshold=1):
    #Ищет транзакции, где было перемещено более threshold биткоинов за последние 24 часа.
    print("Поиск крупных транзакций...")
    base_url = "https://api.blockchair.com/bitcoin/transactions"

    try:
        # Формируем корректный запрос
        params = {
            "limit": 100,  # Получить последние 100 транзакций
            "q": f"value(>{threshold * 1e8})",  # Указываем пороговое значение в сатоши
            "offset": 0,  # Начало выборки
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        transactions = data.get("data", [])

        if not transactions:
            print("Крупных транзакций за последние 24 часа не найдено.")
            return

        for tx in transactions:
            tx_hash = tx.get("transaction_hash", "Неизвестный")
            print(f"Найдена транзакция: {tx_hash}")
            print(f"Сумма: {threshold} BTC")
            print("--------------------------")

    except requests.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

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
#    рух Х монет протягом У годин
    analyze_crypto_changes(symbols, timeframe_hours)

