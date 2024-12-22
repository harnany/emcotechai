### README для проекта YOLOv8 Object Detection

### Описание

Этот проект использует модель YOLOv8 для обнаружения объектов в видеофайлах. Он обрабатывает каждый кадр видео, определяет объекты, рисует рамки вокруг них и добавляет подписи с названиями классов. Обработанное видео сохраняется в новый файл.

### Требования

- Python 3.x

- Библиотеки:

- ultralytics

- opencv-python

- numpy

Вы можете установить необходимые библиотеки с помощью pip:

```
pip install ultralytics opencv-python numpy
```

### Использование

- Скачайте предобученную модель YOLOv8 и сохраните её в корневом каталоге проекта под именем yolov8n.pt.

- Поместите видеофайл, который вы хотите обработать, в корневой каталог проекта и назовите его vidoos.mp4.

- Запустите скрипт:

```
python your_script_name.py
```
- Обработанное видео будет сохранено под именем detect.mp4.

### Код

```
# -*- encoding: utf-8 -*-
from ultralytics import YOLO
import cv2
import numpy as np

# Загрузка модели YOLOv8
model = YOLO('yolov8n.pt')

# Список цветов для различных классов
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]

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

frame_number = 0  # Счетчик кадров

while True:
    # Захват кадра
    ret, frame = capture.read()
    if not ret:
        break

    # Обработка кадра с помощью модели YOLO
    results = model(frame)[0]

    # Получение данных об объектах
    classes_names = results.names
    classes = results.boxes.cls.cpu().numpy()
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

    # Рисование рамок и подписей на кадре
    for class_id, box, conf in zip(classes, boxes, results.boxes.conf):
        if conf > 0.5:
            class_name = classes_names[int(class_id)]
            color = colors[int(class_id) % len(colors)]
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Запись обработанного кадра в выходной файл
    writer.write(frame)

    # Отображение кадра
    cv2.imshow('Processed Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_number += 1
    print(f"Processing frame: {frame_number}")

# Освобождение ресурсов и закрытие окон
capture.release()
writer.release()
cv2.destroyAllWindows()
```

### Примечания

- Убедитесь, что видеофайл имеет правильный формат и кодек, поддерживаемый OpenCV.

- Вы можете изменить порог уверенности (в данном случае 0.5)
