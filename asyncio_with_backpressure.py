import asyncio
import random
import time

queue = []
queue_max_size = 5
produced_count = 0
consumed_count = 0
queue_max = 0
production_complete = False

async def simple_producer(producer_id, num_items):
    global queue, produced_count, queue_max

    for i in range(num_items):

        await asyncio.sleep(random.uniform(0.1, 0.3))

        while len(queue) >= queue_max_size:
            await asyncio.sleep(0.01)

        data = f"{producer_id}-{i + 1}"
        queue.append(data)
        produced_count += 1
        queue_max = max(queue_max, len(queue))

        print(f"Производитель {producer_id} → {data} (очередь: {len(queue)})")

async def simple_consumer(consumer_id):
    global queue, consumed_count, production_complete

    while True:
        if queue:

            data = queue.pop(0)

            await asyncio.sleep(random.uniform(0.2, 0.6))

            consumed_count += 1
            print(f"Потребитель {consumer_id} ← {data} (очередь: {len(queue)})")
        elif production_complete:
            break
        else:
            await asyncio.sleep(0.01)


async def main():
    global production_complete
    print("Система Производитель-Потребитель")
    print("=" * 50)
    start_time = time.time()

    producers = [
        asyncio.create_task(simple_producer(0, 5)),
        asyncio.create_task(simple_producer(1, 5)),
        asyncio.create_task(simple_producer(2, 5))
    ]

    consumers = [
        asyncio.create_task(simple_consumer(0)),
        asyncio.create_task(simple_consumer(1))
    ]

    try:
        await asyncio.gather(*producers)
        print("Все производители завершили работу")

        production_complete = True
        print("Производство завершено, ожидаем обработки оставшихся данных...")

        await asyncio.wait_for(asyncio.gather(*consumers), timeout=10.0)

    except asyncio.CancelledError:
        print("Программа прервана пользователем")
    except asyncio.TimeoutError:
        print("Таймаут ожидания потребителей")
        for consumer in consumers:
            consumer.cancel()
    except KeyboardInterrupt:
        print("Получен сигнал прерывания")
        for task in producers + consumers:
            task.cancel()
        await asyncio.gather(*producers, *consumers, return_exceptions=True)
    finally:
        total_time = time.time() - start_time

        print("=" * 50)
        print(f"Результаты:")
        print(f"Общее время: {total_time:.2f} сек")
        print(f"Произведено элементов: {produced_count}")
        print(f"Обработано элементов: {consumed_count}")
        print(f"Максимальный размер очереди: {queue_max}")
        print(f"Осталось в очереди: {len(queue)} элементов")

        if produced_count == consumed_count:
            print("✅ Все данные успешно обработаны!")
        else:
            print(f"❌ Потеря данных: {produced_count - consumed_count} элементов")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")