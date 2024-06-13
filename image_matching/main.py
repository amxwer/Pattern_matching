import os
#import cv2
from PIL import Image
import imagehash



def load_images_from_directory(directory):
    images = []
    paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpeg') or file.lower().endswith('.jpg'):
                image_path = os.path.join(root, file)
                try:
                    image = Image.open(image_path)
                    images.append(image)
                    paths.append(image_path)
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
    return images, paths


def compute_image_hash(image):
    return imagehash.average_hash(image)


def find_duplicates_by_hash(images, paths):
    hash_dict = {}
    duplicates = []

    for img, path in zip(images, paths):
        img_hash = compute_image_hash(img)
        if img_hash in hash_dict:
            duplicates.append((path, hash_dict[img_hash]))
        else:
            hash_dict[img_hash] = path

    return duplicates


def find_duplicates_in_single_folder(directory):
    images, paths = load_images_from_directory(directory)
    duplicates = find_duplicates_by_hash(images, paths)
    return duplicates


def find_duplicates_between_folders(dir1, dir2):
    images1, paths1 = load_images_from_directory(dir1)
    images2, paths2 = load_images_from_directory(dir2)

    hash_dict = {}
    duplicates = []

    for img, path in zip(images1, paths1):
        img_hash = compute_image_hash(img)
        hash_dict[img_hash] = path

    for img, path in zip(images2, paths2):
        img_hash = compute_image_hash(img)
        if img_hash in hash_dict:
            duplicates.append((path, hash_dict[img_hash]))

    return duplicates


def print_duplicates(duplicates):
    if not duplicates:
        print("Дубликаты не найдены.")
    else:
        print("Найденные дубликаты:")
        for dup in duplicates:
            print(f"{dup[0]} и {dup[1]}")


if __name__ == "__main__":
    folder1 = "D:/5 Flower Types Classification Dataset"
    folder2 = "path/folder2"

    print("Поиск дубликатов в одной папке...")
    duplicates_in_single_folder = find_duplicates_in_single_folder(folder1)
    print_duplicates(duplicates_in_single_folder)

    print("\nПоиск дубликатов между двумя папками...")
    duplicates_between_folders = find_duplicates_between_folders(folder1, folder2)
    print_duplicates(duplicates_between_folders)