import cv2
import numpy as np
from database import BoatDatabase

def adjust_thresholds(image, low_threshold, high_threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)
    blurred = cv2.GaussianBlur(clahe_img, (5, 5), 0)
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    return edges

def find_contours(image, low_threshold=50, high_threshold=150):
    edges = adjust_thresholds(image, low_threshold, high_threshold)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def display_contours(image, contours, denoise, db):
    contour_image = image.copy()
    boat_count = 0

    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)  # Отображение контуров зелёным цветом

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > denoise:  # Убираем маленькие шумы
            boat_count += 1
            x, y, w, h = cv2.boundingRect(contour)
            db.add_coordinate(f'Boat {boat_count}', x, y, w, h, 0)  # Временная метка 0 для примера
            cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(contour_image, f'Boat {boat_count}', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Contours', contour_image)    
    cv2.waitKey(1)  # Задержка в 1 миллисекунду для отображения
    
    return boat_count  # Возвращаем количество лодок

def process_image(image_path, low_threshold, high_threshold, denoise, video_name):
    db = BoatDatabase(video_name)    
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Ошибка загрузки изображения: {image_path}")
        return

    contours = find_contours(image, low_threshold, high_threshold)
    boat_count = display_contours(image, contours, denoise, db)

    if boat_count > 0:
        print(f"Обнаружено лодок: {boat_count}")
        db.save_to_csv()  # Сохраняем координаты из базы данных
    else:
        print("Лодки не обнаружены!")

def main(input_path, low_threshold, high_threshold, denoise):
    # Проверяем, является ли файл изображением
    if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        process_image(input_path, low_threshold, high_threshold, denoise, "single_image")
        cv2.waitKey(0)  # Ожидание, пока не будет нажата клавиша
        cv2.destroyAllWindows()  # Закрытие всех окон
    else:
        print("Формат файла не поддерживается. Ожидается изображение.")

# Пример использования
if __name__ == "__main__":
    input_path = 'image/1.png'  # Замените на ваш путь к изображению
    low_threshold = 100
    high_threshold = 400
    denoise = 300

    main(input_path, low_threshold, high_threshold, denoise)