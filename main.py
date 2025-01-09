import ccxt

programm_version='0.0.0.1'
programm_author = '@syteser'
programm_name = ''

print(f'************************************************')
print(f'HELLO!!!')
print(f'Версія програми - {programm_version}')
print(f'author: {programm_author} 2025')
print(f'************************************************')


def main():
    exchange = ccxt.binance()
    symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"]

    print("Анализ изменения цен за последние 24 часа:")
    for symbol in symbols:
        try:
            ticker = exchange.fetch_ticker(symbol)
            last_price = ticker['last']
            open_price = ticker['open']
            change_percent = ((last_price - open_price) / open_price) * 100
            status = "выросла" if change_percent > 0 else "упала"
            print(f"Монета {symbol.split('/')[0]} {status} на {abs(change_percent):.2f}% за последние 24 часа.")
        except Exception as e:
            print(f"Ошибка при обработке {symbol}: {e}")


import requests

def fetch_large_transactions(threshold=1):
    """
    Ищет транзакции, где было перемещено более threshold биткоинов за последние 24 часа.
    """
    print("Поиск крупных транзакций...")

    # Используем Blockchair API для поиска транзакций
    base_url = "https://api.blockchair.com/bitcoin/transactions"  # Пример API

    try:
        # Параметры запроса: количество записей и временной диапазон
        params = {
            "limit": 100,  # Получить последние 100 транзакций (можно увеличить)
            "q": f"time(utc-now()-24*60*60)..utc-now(),outputs(value(>{threshold}00000000))"
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Проверяем, есть ли данные о транзакциях
        transactions = data.get("data", [])

        if not transactions:
            print("Крупных транзакций за последние 24 часа не найдено.")
            return

        # Анализируем и выводим результаты
        for tx in transactions:
            tx_hash = tx.get("transaction_hash")
            inputs = tx.get("inputs")
            outputs = tx.get("outputs")

            print(f"Транзакция {tx_hash}:")
            print("Входы:")
            for inp in inputs:
                print(f"  Адрес: {inp['recipient']}, Сумма: {int(inp['value']) / 1e8} BTC")

            print("Выходы:")
            for out in outputs:
                print(f"  Адрес: {out['recipient']}, Сумма: {int(out['value']) / 1e8} BTC")

            print("--------------------------")

    except requests.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    main()
    fetch_large_transactions(1)
