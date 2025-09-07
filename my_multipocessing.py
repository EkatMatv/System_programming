# производитель кладет от 1 до 10
# потребитель берет числа из очереди и печатает их квадрат
# когда производитель закончит, кладет STOP
import multiprocessing
import random
import time
from multiprocessing import Process, Queue


def producer(q, count):
    for i in range(1, count + 1):
        num = random.randint(1, 10)
        q.put(num)
        print(f"Производитель положил: {num}")
        time.sleep(0.1)

    q.put("STOP")
    print("Производитель закончил работу")


def consumer(q, consumer_id):

    while True:
        item = q.get()

        if item == "STOP":
            q.put("STOP")  # передаем сигнал следующему потребителю
            print(f"Потребитель {consumer_id} завершил работу")
            break

        result = item ** 2
        print(f"Потребитель {consumer_id} взял: {item}, квадрат: {result}")
        time.sleep(0.2)


if __name__ == "__main__":
    q = multiprocessing.Queue()
    producer_process = Process(
        target=producer,
        args=(q, 15),
        name="Producer"
    )

    consumer_process = Process(
        target=consumer,
        args=(q, 1),
        name="Consumer"
    )

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()my

    print("Все процессы завершили работу!")
