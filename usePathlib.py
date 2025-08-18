from pathlib import Path
import os

def manage_files_and_directories():
    current_dir = Path.cwd()
    print(f"Текущая директория: {current_dir}")

    reports_dir = current_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    print(f"Создана папка: {reports_dir}")

    os.chdir(reports_dir)
    print(f"Текущая директория: {Path.cwd()}")

    summary_file = reports_dir / 'summary.txt'
    files_list = "\n".join(str(item.name) for item in current_dir.iterdir())
    summary_file.write_text(f"Список файлов:\n{files_list}")
    print(f"Файл summary.txt создан в {reports_dir}")

    print("\nСодержимое summary.txt:")
    print(summary_file.read_text())

    print("\nТекстовые файлы (.txt):")
    for txt_file in current_dir.glob('*.txt'):
        file_size = txt_file.stat().st_size  # размер в байтах
        print(f"{txt_file.name} - {file_size} байт")

    print("\nРекурсивный обход файлов:")
    for item in current_dir.rglob("*"):
        print(f"{'Файл' if item.is_file() else 'Папка'}: {item.relative_to(current_dir)}")


if __name__ == "__main__":
    manage_files_and_directories()