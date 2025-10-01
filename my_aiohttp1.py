"""
Необходимо написать асинхронное приложение, которое:
Загружает данные с нескольких API-эндпоинтов (список URL будет задан).
Делает это конкурентно (параллельно с помощью корутин).
Использует пул соединений для экономии ресурсов.
Устанавливает таймауты на каждый запрос, чтобы избежать зависаний.
Собирает результаты всех успешных запросов в единый список (или файл JSON) и выводит статистику:
количество успешных ответов;
количество ошибок (например, таймаутов или HTTP-ошибок);
среднее время отклика.

2. Исходные данные
Пример списка тестовых URL (можно использовать публичные API или заглушки):
URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
    # … добавьте ещё 10–15 URL для нагрузки
]

3. Требования к реализации
Выберите клиент:
либо aiohttp,
либо httpx в асинхронном режиме.

Настройте пул соединений:
например, ограничьте количество одновременных подключений (5–10).

Настройте таймауты:
общий таймаут на выполнение запроса (например, 5 секунд),
таймаут на подключение (например, 2 секунды).

Реализуйте обработку ошибок:
отлавливайте TimeoutError и ошибки HTTP (4xx, 5xx),
учитывайте их в статистике.
Используйте конкурентное выполнение (asyncio.gather или TaskGroup).

По завершении работы:
сохраните успешные ответы в JSON-файл,
выведите статистику (успехи, ошибки, среднее время отклика).
"""
import asyncio, aiohttp, json, time

URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
]


async def fetch(session, url):
    start = time.time()
    try:
        async with session.get(url) as r:
            data = await r.json() if r.status == 200 else None
            return data, time.time() - start, r.status == 200
    except:
        return None, time.time() - start, False


async def main():
    timeout = aiohttp.ClientTimeout(total=5)
    connector = aiohttp.TCPConnector(limit=5)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [fetch(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)

    success = [r[0] for r in results if r[2]]
    times = [r[1] for r in results]

    with open("results.json", "w") as f:
        json.dump(success, f, indent=2)

    print(f"Успешно: {len(success)}")
    print(f"Ошибок: {len(URLS) - len(success)}")
    print(f"Среднее время: {sum(times) / len(times):.2f} сек")


asyncio.run(main())