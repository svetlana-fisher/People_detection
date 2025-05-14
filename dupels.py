from PIL import Image
import imagehash
import os

def remove_duplicates(image_folder):
    hashes = {}
    duplicates = []

    # Проходим по всем изображениям в папке
    for filename in os.listdir(image_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_folder, filename)
            img = Image.open(img_path)
            hash_value = imagehash.phash(img)

            if hash_value in hashes:
                # Если хеш уже существует, добавляем в дубликаты
                duplicates.append(img_path)
            else:
                # Сохраняем оригинал
                hashes[hash_value] = img_path

    # Удаляем дубликаты
    for dup in duplicates:
        os.remove(dup)
        os.remove(dup.replace('.jpg', '.txt'))
        print(f"Удален дубликат: {dup}")

    print("Удаление дубликатов завершено.")

# Укажите путь к вашей папке с изображениями
remove_duplicates('C:\\Users\\sveta\\Documents\\People_detection\\drone_dataset\\images\\train')
