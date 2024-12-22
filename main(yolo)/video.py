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

    return contour_image, boat_count  # Возвращаем изображение с контурами и количество лодок

def process_video(video_path, low_threshold, high_threshold, denoise):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Ошибка открытия видео: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    db = BoatDatabase(video_name=video_path.split('/')[-1].split('.')[0])  # Имя видео для сохранения в CSV

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Нахождение контуров
        contours = find_contours(frame, low_threshold, high_threshold)

        # Подсчет лодок и отображение контуров
        contour_image, boat_count = display_contours(frame, contours, denoise, db)

        # Сохраняем координаты с временной меткой
        if boat_count > 0:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > denoise:  # Убираем маленькие шумы
                    x, y, w, h = cv2.boundingRect(contour)
                    db.add_coordinate(f'Boat {boat_count}', x, y, w, h, frame_count / fps)  # Добавление временной метки

        # Отображаем кадр с контурами
        cv2.imshow('Video Processing', contour_image)

        # Прерывание при нажатии на клавишу 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    db.save_to_csv()
    print("Обработка видео завершена.")

# Запуск функции обработки видео
if __name__ == "__main__":
    process_video('video2.MP4', 100, 400, 300)  # Замените на ваш путь к видео