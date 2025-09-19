"""
Вы создаёте программу, которая:
Загружает данные с нескольких URL (некоторые URL корректные, некоторые вызывают ошибки).
Параллельно выполняет вычисления (например, деление чисел, где могут возникнуть ошибки деления на ноль).
Использует TaskGroup для управления всеми задачами.
Корректно собирает все ошибки в ExceptionGroup.
Гарантирует, что при падении одной задачи остальные корректно отменяются, а ресурсы освобождаются.
urls = [
    "https://httpbin.org/get",        # корректный
    "https://httpbin.org/status/404", # вызовет ошибку 404
    "https://httpbin.org/delay/5",    # имитация долгой загрузки
]

Создайте функцию async fetch_url(session, url), которая:
Загружает страницу с помощью aiohttp.
Если URL возвращает ошибку, она выбрасывается наружу (не ловим внутри).
В блоке finally закрываем соединение (или выводим сообщение о завершении).

Создайте функцию async compute_division(a, b), которая:
Выполняет a / b.
Если b == 0, выбрасывается ZeroDivisionError.
Использует await asyncio.sleep(...) для имитации долгих вычислений.
В блоке finally печатает, что вычисление завершено.

В main() используйте asyncio.TaskGroup для запуска:
Задач на загрузку URL.
Задач на вычисления (например, деление нескольких чисел, где есть деление на ноль).
Оберните TaskGroup в блок try/except* для обработки ошибок:
except* aiohttp.ClientError → вывод ошибок HTTP.
except* ZeroDivisionError → вывод ошибок деления на ноль.
except* asyncio.CancelledError → вывод, что оставшиеся задачи были отменены.

Убедитесь, что:
Если одна задача падает, остальные отменяются.
В finally каждой задачи всегда выполняется очистка/закрытие ресурсов.
Все ошибки собираются и выводятся после завершения TaskGroup."""

import asyncio
import aiohttp
from aiohttp import ClientResponseError

async def fetch_url(session, url):
    try:
        print(f"Начинаем загрузку: {url}")
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.text()
            print(f"Успешно загружено: {url} (длина: {len(data)} символов)")
            return data
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        raise
    finally:
        print(f"Завершение работы с URL: {url}")

async def compute_division(a, b):
    try:
        print(f"Начинаем вычисление: {a} / {b}")
        await asyncio.sleep(1)
        result = a / b
        print(f"Результат вычисления: {result}")
        return result
    except ZeroDivisionError:
        print(f"Ошибка деления на ноль: {a} / {b}")
        raise
    finally:
        print(f"Вычисление завершено: {a} / {b}")

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/status/404",
        "https://httpbin.org/delay/2",
    ]

    computations = [
        (10, 2),
        (5, 0),
        (8, 4),
    ]

    async with aiohttp.ClientSession() as session:
        try:
            async with asyncio.TaskGroup() as tg:

                fetch_tasks = [
                    tg.create_task(fetch_url(session, url))
                    for url in urls
                ]

                compute_tasks = [
                    tg.create_task(compute_division(a, b))
                    for a, b in computations
                ]

                print("Все задачи запущены в TaskGroup")

        except* aiohttp.ClientError as eg:
            print(f"\n=== Ошибки HTTP ===")
            for error in eg.exceptions:
                print(f"HTTP ошибка: {error}")

        except* ZeroDivisionError as eg:
            print(f"\n=== Ошибки деления ===")
            for error in eg.exceptions:
                print(f"Ошибка деления: {error}")

        except* asyncio.CancelledError as eg:
            print(f"\n=== Задачи отменены ===")
            for error in eg.exceptions:
                print(f"Отмененная задача: {error}")

        except* Exception as eg:
            print(f"\n=== Необработанные ошибки ===")
            for error in eg.exceptions:
                print(f"Необработанная ошибка: {error}")

        finally:
            print("\n=== Завершение работы ===")
            print("Все ресурсы освобождены")

if __name__ == "__main__":
    asyncio.run(main())