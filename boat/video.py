import cv2
from database import BoatDatabase
from visual import display_contours, find_contours

def process_video(video_path, low_threshold, high_threshold, denoise):
    cap = cv2.VideoCapture(video_path)
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
        boat_count, coordinates = display_contours(frame, contours, denoise)

        # Сохраняем координаты с временной меткой
        if boat_count > 0:
            for coord in coordinates:
                db.add_coordinate(*coord, timestamp=frame_count / fps)  # Добавление временной метки

        frame_count += 1

    cap.release()
    db.save_to_csv()
    print("Обработка видео завершена.")