# компания занимается обработкой больших тексовых файлов
# вам нужно параллельно:
# загружать тексты
# делить их на части
# считать частоту слов
# сохранять результаты в общий словарь
# синхронизировать доступ к ресурсам
# модульность

import multiprocessing
import re
import os
from collections import Counter
from multiprocessing import Process, Queue, Lock, Value, Manager


def file_loader(file_queue, files):
    """Просто загружает файлы в очередь"""
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                file_queue.put((file_path, content))
                print(f"Загружен: {file_path}")
        except:
            print(f"Ошибка загрузки: {file_path}")

    # Сигнал завершения для каждого воркера
    for _ in range(4):
        file_queue.put((None, None))


def text_worker(file_queue, word_freq, lock, counter):
    """Обрабатывает тексты и считает слова"""
    while True:
        file_path, content = file_queue.get()

        if file_path is None:  # Сигнал завершения
            break

        # Считаем слова
        words = re.findall(r'\w+', content.lower())

        # Обновляем общий словарь с блокировкой
        with lock:
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Увеличиваем счетчик
        with counter.get_lock():
            counter.value += 1

        print(f"Обработан: {file_path} ({len(words)} слов)")


def main():
    # Создаем тестовые файлы
    sample_texts = [
        "hello world python programming",
        "multiprocessing in python is useful",
        "text analysis with python",
        "simple word counting example"
    ]

    files = []
    for i, text in enumerate(sample_texts):
        filename = f"text_{i}.txt"
        with open(filename, 'w') as f:
            f.write(text)
        files.append(filename)

    # Создаем общие объекты
    with Manager() as manager:
        file_queue = Queue()
        word_freq = manager.dict()
        lock = Lock()
        counter = Value('i', 0)

        # Запускаем загрузчик
        loader = Process(target=file_loader, args=(file_queue, files))
        loader.start()

        # Запускаем воркеры
        workers = []
        for i in range(4):  # 4 рабочих процесса
            worker = Process(target=text_worker, args=(file_queue, word_freq, lock, counter))
            workers.append(worker)
            worker.start()

        # Ждем завершения
        loader.join()
        for worker in workers:
            worker.join()

        # Выводим результаты
        print(f"\nОбработано файлов: {counter.value}")
        print("Топ-10 слов:")
        for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {word}: {count}")

    # Удаляем временные файлы
    for file in files:
        os.remove(file)


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()