import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    
    return edges

def find_contours(image, low_threshold=50, high_threshold=150):
    edges = adjust_thresholds(image, low_threshold, high_threshold)
    # Обнаружение контуров
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def display_contours(image, contours):
    # Отображение результатов
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    cv2.imshow('Contours', contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(image_path, low_threshold, high_threshold):
    # Загрузка изображения
    image = cv2.imread(image_path)
    
    # Нахождение контуров
    contours = find_contours(image, low_threshold, high_threshold)
    
    # Проверяем количество контуров
    if len(contours) > 100:  # Пример "слишком много контуров"
        print("Слишком много контуров обнаружено!")
    elif len(contours) == 0:  # Пример "слишком мало контуров"
        print("Контуры не обнаружены!")
    else:
        print(f"Обнаружено контуров: {len(contours)}")
    
    # Отображаем количество контуров
    display_contours(image, contours)

# Увеличение порогового значения
def increase_thresholds(low_threshold, high_threshold):
    return low_threshold + 10, high_threshold + 10

# Уменьшение порогового значения
def decrease_thresholds(low_threshold, high_threshold):
    return max(0, low_threshold - 10), max(0, high_threshold - 10)

# Пример использования
if __name__ == "__main__":
    image_path = 'image/2.jpg'  # Замените на ваш путь к изображению
    low_threshold = 300
    high_threshold = 400
    
    main(image_path, low_threshold, high_threshold)  # Обычный случай