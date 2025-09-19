"""Вам нужно реализовать асинхронную программу, которая:
Загружает содержимое с нескольких URL-адресов (например, страницы
https://httpbin.org/delay/X, где X — это задержка).
Одновременно выполняет не более трёх запросов. Для ограничения используйте
asyncio.Semaphore.

Для каждого успешно завершённого запроса выводит сообщение вида:
Успешно загружено: <url>, длина ответа = <число символов>

Если при загрузке возникает ошибка (aiohttp.ClientError или таймаут),
нужно обработать её и вывести сообщение:
Ошибка при загрузке: <url>, причина: <текст ошибки>

После завершения всех запросов программа должна вывести общее количество
успешно обработанных URL и количество ошибок."""

import asyncio
import aiohttp
from aiohttp import ClientTimeout

async def fetch_url(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                response.raise_for_status()
                data = await response.text()
                print(f"Успешно загружено: {url}, длина ответа = {len(data)} символов")
                return {"status": "success", "url": url, "length": len(data)}

        except asyncio.TimeoutError:
            error_msg = f"Таймаут при загрузке"
            print(f"Ошибка при загрузке: {url}, причина: {error_msg}")
            return {"status": "error", "url": url, "error": error_msg}

        except aiohttp.ClientError as e:
            error_msg = str(e)
            print(f"Ошибка при загрузке: {url}, причина: {error_msg}")
            return {"status": "error", "url": url, "error": error_msg}

        except Exception as e:
            error_msg = f"Неизвестная ошибка: {e}"
            print(f"Ошибка при загрузке: {url}, причина: {error_msg}")
            return {"status": "error", "url": url, "error": error_msg}


async def main():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/404",
        "https://httpbin.org/delay/2",
        "https://invalid-url-12345.com",
        "https://httpbin.org/delay/1"
    ]

    semaphore = asyncio.Semaphore(3)

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch_url(session, url, semaphore)
            for url in urls
        ]

        results = await asyncio.gather(*tasks)

        success_count = sum(1 for result in results if result["status"] == "success")
        error_count = sum(1 for result in results if result["status"] == "error")

        print(f"\n=== Результаты ===")
        print(f"Всего URL: {len(urls)}")
        print(f"Успешно обработано: {success_count}")
        print(f"Ошибок: {error_count}")

        # Дополнительная информация об успешных запросах
        if success_count > 0:
            print(f"\nУспешные запросы:")
            for result in results:
                if result["status"] == "success":
                    print(f"  - {result['url']}: {result['length']} символов")

        if error_count > 0:
            print(f"\nОшибочные запросы:")
            for result in results:
                if result["status"] == "error":
                    print(f"  - {result['url']}: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())