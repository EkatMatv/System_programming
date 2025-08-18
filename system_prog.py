"""
1. Работа с текущей директорией
Получите текущую рабочую директорию.
Создайте в ней папку backup.
Перейдите в созданную папку.
os.getcwd(), os.mkdir(), os.chdir()

2. Сканирование папки
Вернитесь в исходную директорию.
Получите список всех файлов и папок в директории.
Отфильтруйте только файлы.
os.isfile() os.listdir(), os.path.isfile(), os.path.join()

3. Копирование файлов (эмуляция)
Для каждого файла из пункта 2:
Получите его размер.
Создайте копию с добавлением постфикса _backup в папке backup (только симуляция, без shutil, можно просто создать пустой файл с новым именем).
os.path.getsize(), open(), os.path.basename(), os.path.splitext()

4. Вывод информации о системе
Определите имя операционной системы.
Получите значение переменной окружения HOME или USERPROFILE (в зависимости от ОС).
Выведите PID текущего процесса.
os.name, os.environ.get(), os.getpid()
"""
import os

def create_backup_folder(path):
    """Создаёт папку backup и переходит в неё"""
    backup_path = os.path.join(path, 'backup')
    try:
        os.mkdir(backup_path)
    except FileExistsError:
        pass
    os.chdir(backup_path)
    print(f"Перешли в папку: {os.getcwd()}")
    return backup_path


def list_files(path):
    """Возвращает список только файлов (без папок)"""
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            files.append(item)
    print(f"Найдены файлы: {files}")
    return files


def simulate_backup(files, dest_folder):
    """Создаёт копии файлов с '_backup' в имени"""
    for filename in files:

        file_size = os.path.getsize(filename)
        print(f"Файл: {filename}, Размер: {file_size} байт")

        base_name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        backup_name = f"{base_name}_backup{extension}"

        with open(os.path.join(dest_folder, backup_name), 'w') as f:
            pass
        print(f"Создана копия: {backup_name}")


def show_system_info():
    """Выводит информацию о системе"""
    os_type = os.name
    home_var = 'USERPROFILE' if os_type == 'nt' else 'HOME'

    print("\nИнформация о системе:")
    print(f"Тип ОС: {os_type}")
    print(f"Домашняя директория: {os.environ.get(home_var)}")
    print(f"PID текущего процесса: {os.getpid()}")


if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")

    backup_dir = create_backup_folder(current_dir)

    os.chdir(current_dir)
    files = list_files(current_dir)

    simulate_backup(files, backup_dir)

    show_system_info()