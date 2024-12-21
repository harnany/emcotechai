import cv2
import numpy as np
from database import BoatDatabase
from video import process_video
from visual import display_contours, find_contours  # Импортируем find_contours

def main(image_path, low_threshold, high_threshold, denoise):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Нахождение контуров
    contours = find_contours(image, low_threshold, high_threshold)

    # Подсчет лодок и отображение контуров
    boat_count, coordinates = display_contours(image, contours, denoise)

    # Печатаем количество лодок
    if boat_count > 0:
        print(f"Обнаружено лодок: {boat_count}")
        # Сохраняем координаты лодок в CSV
        db = BoatDatabase("my_video")  # Меняем название на соответствующее
        for coord in coordinates:
            db.add_coordinate(*coord, timestamp=0)  # Вам нужно будет передать реальную временную метку
        db.save_to_csv()
    else:
        print("Лодки не обнаружены!")

# Пример использования
if __name__ == "__main__":
    image_path = 'image/1.png'  # Замените на ваш путь к изображению
    low_threshold = 100
    high_threshold = 400
    denoise = 300

    main(image_path, low_threshold, high_threshold, denoise)