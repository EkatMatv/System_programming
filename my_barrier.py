import threading
import queue
import time
import random

NUM_WORKERS = 2
TOTAL_TASKS = 6

task_queue = queue.Queue()
start_barrier = threading.Barrier(NUM_WORKERS + 1)
completion_barrier = threading.Barrier(NUM_WORKERS + 1)

def producer():
    print("Производитель: ожидаю старта рабочих...")
    start_barrier.wait()

    print("Производитель: начинаю создание задач")
    for i in range(TOTAL_TASKS):
        task = f"Task-{i + 1}"
        task_queue.put(task)
        print(f"Производитель: создал {task}")
        time.sleep(0.1)

    for _ in range(NUM_WORKERS):
        task_queue.put(None)

    print("Производитель: задачи созданы, ожидаю завершения...")
    completion_barrier.wait()
    print("Производитель: работа завершена")


def worker(worker_id):
    print(f"Рабочий-{worker_id}: готов к старту")
    start_barrier.wait()

    print(f"Рабочий-{worker_id}: начинаю работу")
    count = 0

    while True:
        task = task_queue.get()
        if task is None:
            task_queue.task_done()
            break

        print(f"Рабочий-{worker_id}: обрабатываю {task}")
        time.sleep(random.uniform(0.3, 0.6))
        print(f"Рабочий-{worker_id}: завершил {task}")
        count += 1
        task_queue.task_done()

    print(f"Рабочий-{worker_id}: обработал {count} задач")
    completion_barrier.wait()
    print(f"Рабочий-{worker_id}: завершил работу")


threads = []
producer_thread = threading.Thread(target=producer)
threads.append(producer_thread)
producer_thread.start()

for i in range(NUM_WORKERS):
    t = threading.Thread(target=worker, args=(i + 1,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

task_queue.join()
print("Работа завершена!")