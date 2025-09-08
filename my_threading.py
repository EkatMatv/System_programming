import threading
import time

buffer = []
max_size = 5
lock = threading.Lock()
not_empty = threading.Condition(lock)
not_full = threading.Condition(lock)

def producer():
    for i in range(1, 21):
        with lock:
            while len(buffer) >= max_size:
                print(f"{threading.current_thread().name}: Буфер полон, жду...")
                not_full.wait()

            buffer.append(i)
            print(f"{threading.current_thread().name}: Добавил {i}, буфер: {buffer}")
            not_empty.notify()

def consumer():
    for _ in range(20):
        with lock:
            while len(buffer) == 0:
                print(f"{threading.current_thread().name}: Буфер пуст, жду...")
                not_empty.wait()

            item = buffer.pop(0)
            print(f"{threading.current_thread().name}: Извлек {item}, буфер: {buffer}")
            not_full.notify()

prod = threading.Thread(target=producer, name="Производитель")
cons = threading.Thread(target=consumer, name="Потребитель")

prod.start()
cons.start()

prod.join()
cons.join()
