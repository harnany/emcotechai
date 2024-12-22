# -*- encoding: utf-8 -*-
from ultralytics import YOLO
import cv2
import numpy as np
import csv

# �������� ������ YOLOv8
model = YOLO('yolov8n.pt')

# ������ ������ ��� ��������� �������
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]

# ������ ������ ��� ����� (�������� �� ���������� ������ ����� ������)
boat_class_id = 0

# �������� ��������� ����������
input_video_path = 'vidoos.mp4'
capture = cv2.VideoCapture(input_video_path)

# ������ ���������� �����
fps = int(capture.get(cv2.CAP_PROP_FPS))
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ��������� ��������� �����
output_video_path = 'detect.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # ����� ����������� 'XVID'
writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# �������� CSV ����� ��� ������ ������
with open('detection_data.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Frame', 'Class', 'Confidence', 'X1', 'Y1', 'X2', 'Y2'])  # ��������� ��������

    last_boat_box = None  # ��������� ��������� ����� ��� �����
    frame_number = 0  # ������� ������

    while True:
        # ������ �����
        ret, frame = capture.read()
        if not ret:
            break

        # ��������� ����� � ������� ������ YOLO
        results = model(frame)[0]

        classes_names = results.names
        classes = results.boxes.cls.cpu().numpy()
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

        # ���������� ��� ������������, ���� �� ����� ����������
        boat_found = False

        # ��������� ����� � �������� �� �����
        for class_id, box, conf in zip(classes, boxes, results.boxes.conf):
            if class_id == boat_class_id and conf > 0.5:  # ��������, ��� ������� �����
                boat_found = True
                class_name = classes_names[int(class_id)]
                color = colors[int(class_id) % len(colors)]
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # ������ ������ � CSV ����
                csv_writer.writerow([frame_number, class_name, conf.item(), x1, y1, x2, y2])
                print(f"Frame: {frame_number}, Class: {class_name}, Confidence: {conf.item()}, Box: [{x1}, {y1}, {x2}, {y2}]")  # ���������� �����

                last_boat_box = box  # ��������� ����� �����
        
        # ���� ����� �� �������, �� �� ��������� � ��������� �����, ������ �
        if not boat_found and last_boat_box is not None:
            x1, y1, x2, y2 = last_boat_box
            color = colors[boat_class_id % len(colors)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, 'Boat', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # ������ ������������� ����� � �������� ����
        writer.write(frame)

        # ����������� �����
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_number += 1
        print(f"Processing frame: {frame_number}")  # ���������� �����

# ������������ �������� � �������� ����
capture.release()
writer.release()
cv2.destroyAllWindows()