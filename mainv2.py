import cv2
import numpy as np
from database import save_coordinates

def adjust_thresholds(image, low_threshold, high_threshold):
    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)

    # Применение размытия
    blurred = cv2.GaussianBlur(clahe_img, (5, 5), 0)

    # Применение Canny Edge Detection с заданными порогами
    edges = cv2.Canny(blurred, low_threshold, high_threshold)

    return edges, blurred  # Возвращаем размазанное изображение для отладки

def find_contours(image, low_threshold, high_threshold):
    edges, blurred = adjust_thresholds(image, low_threshold, high_threshold)
    # Обнаружение контуров
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Отладочный вывод
    cv2.imshow('Blurred', blurred)
    cv2.imshow('Edges', edges)  # Показываем изображение с краями
    print(f"Найдено контуров: {len(contours)}")

    return contours

def count_boats(image, sensitivity, low_threshold, high_threshold):
    # Нахождение контуров
    contours = find_contours(image, low_threshold, high_threshold)

    boat_count = 0
    coordinates = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Убираем маленькие шумы
            boat_count += 1
            x, y, w, h = cv2.boundingRect(contour)
            coordinates.append((x, y, w, h))

            # Отрисовываем красный контур
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)
            # Отрисовываем зеленый прямоугольник и подписываем номер лодки
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, f'ЛОДКА {boat_count}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return boat_count, coordinates

def main():
    # Загружаем изображение
    image = cv2.imread('image/2.jpg')  # Замените на свой путь к изображению

    # Параметры чувствительности и порогов
    sensitivity = 1  # Для бинаризации
    low_threshold = 300  # Низкий порог для Canny
    high_threshold = 400  # Высокий порог для Canny

    boat_count, coordinates = count_boats(image, sensitivity, low_threshold, high_threshold)

    # Отображаем итоговое изображение с лодками
    cv2.putText(image, f'TOTAL: {boat_count}', (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('Boats', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Сохраняем координаты лодок в CSV
    save_coordinates(coordinates)

if __name__ == '__main__':
    main()