import os
from PIL import Image
import imagehash
import argparse


def load_image_hashes_from_directory(directory):
    """Загрузить хеши изображений из указанной директории.

    Args:
        directory (str): Путь к директории для сканирования изображений.

    Returns:
        dict: Словарь с хешами изображений в качестве ключей и путями к файлам в качестве значений.
    """
    hash_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpeg', '.jpg')):
                image_path = os.path.join(root, file)
                try:
                    with Image.open(image_path) as image:
                        img_hash = compute_image_hash(image)
                        if img_hash in hash_dict:
                            hash_dict[img_hash].append(image_path)
                        else:
                            hash_dict[img_hash] = [image_path]
                except Exception as e:
                    print(f"Ошибка при загрузке изображения {image_path}: {e}")
    return hash_dict


def compute_image_hash(image):
    """Вычислить средний хеш изображения.

    Args:
        image (PIL.Image.Image): Изображение для хеширования.

    Returns:
        ImageHash: Вычисленный хеш изображения.
    """
    return imagehash.average_hash(image)


def find_duplicates(hash_dict1, hash_dict2=None):
    """Найти дубликаты в одном хеш-словаре или между двумя хеш-словарями.

    Args:
        hash_dict1 (dict): Первый хеш-словарь.
        hash_dict2 (dict, optional): Второй хеш-словарь. Если None, используется только hash_dict1.

    Returns:
        list: Список кортежей, содержащих пути дубликатов изображений.
    """
    duplicates = []

    if hash_dict2 is None:
        # Поиск дубликатов в одном хеш-словаре
        for paths in hash_dict1.values():
            if len(paths) > 1:
                for i in range(len(paths)):
                    for j in range(i + 1, len(paths)):
                        duplicates.append((paths[i], paths[j]))
    else:
        # Поиск дубликатов между двумя хеш-словарями
        for img_hash, paths1 in hash_dict1.items():
            if img_hash in hash_dict2:
                for path1 in paths1:
                    for path2 in hash_dict2[img_hash]:
                        duplicates.append((path1, path2))

    return duplicates


def print_duplicates(duplicates):
    """Вывести пути дубликатов изображений.

    Args:
        duplicates (list): Список кортежей, содержащих пути дубликатов изображений.
    """
    if not duplicates:
        print("Дубликаты не найдены.")
    else:
        print("Найденные дубликаты:")
        for dup in duplicates:
            print(f"{dup[0]} и {dup[1]}")


def main(single_folder=None, folder1=None, folder2=None):
    if single_folder:
        print("Поиск дубликатов в одной папке...")
        hash_dict = load_image_hashes_from_directory(single_folder)
        duplicates = find_duplicates(hash_dict)
        print_duplicates(duplicates)
    elif folder1 and folder2:
        print("Поиск дубликатов между двумя папками...")
        hash_dict1 = load_image_hashes_from_directory(folder1)
        hash_dict2 = load_image_hashes_from_directory(folder2)
        duplicates = find_duplicates(hash_dict1, hash_dict2)
        print_duplicates(duplicates)
    else:
        print("Недопустимые аргументы. Пожалуйста, укажите либо одну папку, либо две папки для сравнения.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Найти дубликаты изображений в папках.")
    parser.add_argument('--single_folder', type=str, help="Путь к папке для проверки дубликатов.")
    parser.add_argument('--folder1', type=str, help="Путь к первой папке.")
    parser.add_argument('--folder2', type=str, help="Путь ко второй папке.")

    args = parser.parse_args()

    main(single_folder=args.single_folder, folder1=args.folder1, folder2=args.folder2)