import os
import shutil
import asyncio
import logging
from argparse import ArgumentParser
from pathlib import Path
from colorama import Fore, Style, init

# Ініціалізація colorama для підтримки кольорів у Windows
init(autoreset=True)

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Асинхронна функція для копіювання файлів
async def copy_file(file_path: Path, output_folder: Path):
    try:
        # Отримуємо розширення файлу
        file_extension = file_path.suffix[1:].lower()

        # Створюємо відповідну папку для файлів з таким розширенням
        folder_for_extension = output_folder / file_extension
        folder_for_extension.mkdir(parents=True, exist_ok=True)

        # Визначаємо шлях для нового файлу
        destination = folder_for_extension / file_path.name

        # Копіюємо файл
        shutil.copy(file_path, destination)
        logger.info(f"{Fore.GREEN}Файл {file_path} успішно скопійовано до {destination}")
    except Exception as e:
        logger.error(f"{Fore.RED}Помилка при копіюванні файлу {file_path}: {e}")

# Асинхронна функція для читання файлів з вихідної папки
async def read_folder(source_folder: Path, output_folder: Path):
    try:
        # Проходимо по всіх файлах у папці та підпапках
        for file_path in source_folder.rglob('*'):
            if file_path.is_file():
                await copy_file(file_path, output_folder)
    except Exception as e:
        logger.error(f"{Fore.RED}Помилка при читанні папки {source_folder}: {e}")

# Головна функція для запуску
async def main():
    # Налаштування парсера аргументів командного рядка
    parser = ArgumentParser(description="Сортування файлів за розширенням.")
    parser.add_argument("--source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("--output", type=str, help="Шлях до цільової папки")

    # Парсимо аргументи
    args = parser.parse_args()

    # Якщо шляхи не передані як аргументи, запитуємо їх у користувача
    source_folder = Path(args.source) if args.source else Path(input(f"{Fore.YELLOW}Введіть шлях до вихідної папки: {Style.RESET_ALL}"))
    output_folder = Path(args.output) if args.output else Path(input(f"{Fore.YELLOW}Введіть шлях до цільової папки: {Style.RESET_ALL}"))

    # Перевіряємо, чи існує вихідна папка
    if not source_folder.is_dir():
        logger.error(f"{Fore.RED}Вихідна папка {source_folder} не існує!")
        return

    # Створюємо цільову папку, якщо її не існує
    output_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"{Fore.YELLOW}Починаємо сортування файлів...")

    # Запускаємо асинхронне читання папки
    await read_folder(source_folder, output_folder)

    logger.info(f"{Fore.GREEN}Сортування завершено успішно!")

# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(main())
