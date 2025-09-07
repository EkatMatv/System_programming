# берёт список чисел [5, 7, -3, 8, 10]
# запускает пул процессов для вычисления факториала каждого числа
# если число отрицательное - выбрасывается исключение
# результаты успешных вычислений собираются в список через callback
# ошибки обрабатываются отдельно через error_callback
import multiprocessing
import math
from multiprocessing import Pool
import time

def calculate_factorial(number):

    if number < 0:
        raise ValueError(f"Отрицательное число: {number}. Факториал не определен для отрицательных чисел.")

    time.sleep(0.5)

    return math.factorial(number)

def success_callback(result):
    print(f"Успешно вычислен факториал: {result}")
    successful_results.append(result)


def error_callback(error):
    """Callback функция для обработки ошибок"""
    print(f"Ошибка: {error}")
    errors.append(error)


def main():
    numbers = [5, 7, -3, 8, 10]

    print(f"Исходный список чисел: {numbers}")
    print("Запуск вычислений...")

    with Pool(processes=multiprocessing.cpu_count()) as pool:

        async_results = []
        for number in numbers:
            async_result = pool.apply_async(
                calculate_factorial,
                args=(number,),
                callback=success_callback,
                error_callback=error_callback
            )
            async_results.append(async_result)

        pool.close()
        pool.join()

    print("\n ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Успешные вычисления: {successful_results}")
    print(f"Ошибки: {len(errors)}")

    for error in errors:
        print(f"   - {error}")

if __name__ == "__main__":

    global successful_results, errors
    successful_results = []
    errors = []

    main()