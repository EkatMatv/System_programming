import time
import asyncio
import requests
import aiohttp
import httpx

urls = [
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
]

def fetch_requests(urls):
    start = time.time()
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            print(f"✓ {url} - {response.status_code}")
        except Exception as e:
            print(f"✗ {url} - {e}")
    return time.time() - start

async def fetch_aiohttp(urls):
    start = time.time()
    successful = 0

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        async def fetch_one(url):
            try:
                async with session.get(url) as response:
                    await response.read()
                    print(f"✓ {url} - {response.status}")
                    return 1
            except Exception as e:
                print(f"✗ {url} - {e}")
                return 0

        tasks = [fetch_one(url) for url in urls]
        results = await asyncio.gather(*tasks)
        successful = sum(results)

    return time.time() - start

async def fetch_httpx(urls):
    start = time.time()
    successful = 0

    async with httpx.AsyncClient(timeout=30.0) as client:
        async def fetch_one(url):
            try:
                response = await client.get(url)
                print(f"{url} - {response.status_code}")
                return 1
            except Exception as e:
                print(f"{url} - {e}")
                return 0

        tasks = [fetch_one(url) for url in urls]
        results = await asyncio.gather(*tasks)
        successful = sum(results)

    return time.time() - start


# Главная функция
async def main():

    print("1. REQUESTS (синхронный):")
    time1 = fetch_requests(urls)

    print("\n2. AIOHTTP (асинхронный):")
    time2 = await fetch_aiohttp(urls)

    print("\n3. HTTPX (асинхронный):")
    time3 = await fetch_httpx(urls)

    print("РЕЗУЛЬТАТЫ:")
    print(f"Requests: {time1:.2f} сек")
    print(f"Aiohttp:  {time2:.2f} сек")
    print(f"Httpx:    {time3:.2f} сек")

    times = [time1, time2, time3]
    names = ["Requests", "Aiohttp", "Httpx"]
    fastest = min(times)
    winner = names[times.index(fastest)]

    print(f"\nСамый быстрый: {winner} ({fastest:.2f} сек)")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())