import cv2
import numpy as np

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
    # Копируем изображение для отрисовки
    contour_image = image.copy()
    
    boat_count = 0
    coordinates = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > denoise:  # Убираем маленькие шумы, вы можете изменить это значение
            boat_count += 1
            # Получаем прямоугольник вокруг контура
            x, y, w, h = cv2.boundingRect(contour)
            coordinates.append((x, y, w, h))

            # Отрисовываем красный прямоугольник
            cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Добавляем текст с номером лодки
            cv2.putText(contour_image, f'Boat {boat_count}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Отображаем результат
    cv2.imshow('Contours', contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return boat_count, coordinates

def main(image_path, low_threshold, high_threshold):
    # Загрузка изображения
    image = cv2.imread(image_path)
    
    # Нахождение контуров
    contours = find_contours(image, low_threshold, high_threshold)
    
    # Подсчет лодок и отображение контуров
    boat_count, coordinates = display_contours(image, contours)
    
    # Печатаем количество лодок
    if boat_count > 0:
        print(f"Обнаружено лодок: {boat_count}")
    else:
        print("Лодки не обнаружены!")

# Пример использования
if __name__ == "__main__":
    image_path = 'image/1.png'  # Замените на ваш путь к изображению
    low_threshold = 100
    high_threshold = 400
    denoise = 300
    
    main(image_path, low_threshold, high_threshold)
