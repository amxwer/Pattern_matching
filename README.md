# Поиск дубликатов изображений

Этот скрипт помогает находить дубликаты изображений в одной папке или между двумя папками.

## Установка

1. Клонируйте репозиторий.
2. Библиотеки `Pillow` и `ImageHash`. Установка с помощью pip:
    ```
    pip install Pillow imagehash
    ```

## Использование

Для поиска дубликатов в одной папке:
```bash
python find_duplicates.py --single_folder <путь_к_папке>
````

Для поиска дубликатов между двумя папками:
```` bash
python find_duplicates.py --folder1 <путь_к_первой_папке> --folder2 <путь_ко_второй_папке>
````
