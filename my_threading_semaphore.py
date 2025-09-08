# работа с общим складом
# ограниченное количество ресурсов 5 единиц
# поток = сотрудник, пытается взять ресурс, поработать с ним и вернуть его обратно
# нужна синхронизация
# lock Для количества выполненных операция
# rlock Для функции, которая вызывает внутри себя другую функцию и обе их используют одну и ту же блокировку
# semaphore Ограничить число потоков
# bounded semaphore поменять на
# thread
# вывести сообщение с именем потока и номером операции
# взять ресурс, подождать
# вернуть ресурс, обновить общий счетчик

import threading
import time
import random

resources = 5
resource_lock = threading.Semaphore(5)
counter = 0
counter_lock = threading.Lock()


def simple_worker(worker_name, operations=3):
    global counter, resources

    for i in range(operations):

        print(f"{worker_name}: ждет ресурс для операции {i + 1}")
        resource_lock.acquire()
        resources -= 1
        print(f"{worker_name}: взял ресурс (осталось {resources})")

        time.sleep(random.uniform(0.5, 1.0))
        print(f"{worker_name}: завершил операцию {i + 1}")

        with counter_lock:
            counter += 1
            print(f"{worker_name}: общий счетчик = {counter}")

        resources += 1
        resource_lock.release()
        print(f"{worker_name}: вернул ресурс (теперь {resources})")

    print(f"{worker_name}: закончил работу")


threads = []
for i in range(4):
    t = threading.Thread(target=simple_worker, args=(f"Сотрудник-{i + 1}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Всего выполнено операций: {counter}")