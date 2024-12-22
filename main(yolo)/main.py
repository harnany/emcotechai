# -*- encoding: utf-8 -*-
from ultralytics import YOLO
import cv2
import numpy as np
import csv

# Загрузка модели YOLOv8
model = YOLO('yolov8n.pt')

# Список цветов для различных классов
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]

# Индекс класса для лодки (измените на правильный индекс вашей модели)
boat_class_id = 0

# Открытие исходного видеофайла
input_video_path = 'vidoos.mp4'
capture = cv2.VideoCapture(input_video_path)

# Чтение параметров видео
fps = int(capture.get(cv2.CAP_PROP_FPS))
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Настройка выходного файла
output_video_path = 'detect.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Можно попробовать 'XVID'
writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Открытие CSV файла для записи данных
with open('detection_data.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Frame', 'Class', 'Confidence', 'X1', 'Y1', 'X2', 'Y2'])  # Заголовки столбцов

    last_boat_box = None  # Последняя известная рамка для лодки
    frame_number = 0  # Счетчик кадров

    while True:
        # Захват кадра
        ret, frame = capture.read()
        if not ret:
            break

        # Обработка кадра с помощью модели YOLO
        results = model(frame)[0]

        classes_names = results.names
        classes = results.boxes.cls.cpu().numpy()
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

        # Переменная для отслеживания, была ли лодка обнаружена
        boat_found = False

        # Рисование рамок и подписей на кадре
        for class_id, box, conf in zip(classes, boxes, results.boxes.conf):
            if class_id == boat_class_id and conf > 0.5:  # Убедимся, что находим лодку
                boat_found = True
                class_name = classes_names[int(class_id)]
                color = colors[int(class_id) % len(colors)]
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Запись данных в CSV файл
                csv_writer.writerow([frame_number, class_name, conf.item(), x1, y1, x2, y2])
                print(f"Frame: {frame_number}, Class: {class_name}, Confidence: {conf.item()}, Box: [{x1}, {y1}, {x2}, {y2}]")  # Отладочный вывод

                last_boat_box = box  # Сохраняем рамку лодки
        
        # Если лодка не найдена, но мы сохранили её последнюю рамку, рисуем её
        if not boat_found and last_boat_box is not None:
            x1, y1, x2, y2 = last_boat_box
            color = colors[boat_class_id % len(colors)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, 'Boat', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Запись обработанного кадра в выходной файл
        writer.write(frame)

        # Отображение кадра
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_number += 1
        print(f"Processing frame: {frame_number}")  # Отладочный вывод

# Освобождение ресурсов и закрытие окон
capture.release()
writer.release()
cv2.destroyAllWindows()