import cv2
import pandas as pd
import numpy as np

def display_boat_positions(image_path, csv_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Ошибка загрузки изображения. Проверьте, правильный ли путь и существует ли файл.")
        return

    try:
        df = pd.read_csv(csv_path, sep=';')
    except Exception as e:
        print(f"Ошибка загрузки CSV файла: {e}")
        return

    required_columns = ['boat_id', 'x', 'y', 'width', 'height', 'timestamp']
    for col in required_columns:
        if col not in df.columns:
            print(f"Ошибка: Недостаточно информации в CSV. Убедитесь, что имеется столбец '{col}'.")
            return

    boat_counts = df['boat_id'].value_counts()
    valid_boats = boat_counts[boat_counts >= 10].index.tolist()  # Лодки, которые существуют больше 10 кадров

    color_map = {}
    previous_positions = {}  # Словарь для хранения предыдущих позиций лодок

    for index, row in df.iterrows():
        boat_id = row['boat_id']  # boat_id как строка (например, 'boat 1')
        if boat_id not in valid_boats:
            continue  # Пропускаем лодки, которые не подходят

        try:
            x = int(row['x'])
            y = int(row['y'])
            width = int(row['width'])
            height = int(row['height'])

            # Генерируем уникальный цвет для лодки
            if boat_id not in color_map:
                color_map[boat_id] = tuple(np.random.randint(0, 256, size=3).tolist())

            color = color_map[boat_id]
            # Рисуем точку в центре лодки
            center_position = (x + width // 2, y + height // 2)
            cv2.circle(image, center_position, 5, color, -1)

            # Рисуем траекторию
            if boat_id in previous_positions:
                previous_position = previous_positions[boat_id]
                cv2.line(image, previous_position, center_position, color, 2)  # Рисуем линию

            # Обновляем предыдущую позицию
            previous_positions[boat_id] = center_position

        except Exception as e:
            print(f"Ошибка обработки строки {index}: {e}")
            continue

    cv2.imshow('Boat Positions', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Укажите пути к вашему изображению и CSV-файлу
image_path = 'testVis.jpg'  # Путь к изображению
csv_path = 'test.csv'  # Путь к CSV-файлу

display_boat_positions(image_path, csv_path)