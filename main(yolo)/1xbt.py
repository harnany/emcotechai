import cv2
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future_positions(previous_positions, steps=5):
    """
    Предсказывает будущие позиции на основе предыдущих позиций.
    :param previous_positions: Список предыдущих координат лодки
    :param steps: Количество предсказанных шагов
    :return: Список предсказанных позиций
    """
    if len(previous_positions) < 2:
        return []

    X = np.array(range(len(previous_positions))).reshape(-1, 1)  # Временные метки
    y_x = np.array([pos[0] for pos in previous_positions])  # X-координаты
    y_y = np.array([pos[1] for pos in previous_positions])  # Y-координаты

    model_x = LinearRegression().fit(X, y_x)
    model_y = LinearRegression().fit(X, y_y)

    future_positions = []
    for step in range(1, steps + 1):
        next_x = model_x.predict([[len(previous_positions) + step]])[0]
        next_y = model_y.predict([[len(previous_positions) + step]])[0]
        future_positions.append((next_x, next_y))

    return future_positions

def display_boat_positions(image_path, csv_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Ошибка загрузки изображения. Проверьте правильный ли путь и существует ли файл.")
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
    valid_boats = boat_counts[boat_counts >= 2].index.tolist()  # Лодки, которые существуют больше 2 кадров

    color_map = {}
    previous_positions = {}

    for index, row in df.iterrows():
        boat_id = row['boat_id']
        if boat_id not in valid_boats:
            continue
        
        try:
            x = float(row['x'])  # Убедитесь, что конвертируете в float
            y = float(row['y'])
            width = float(row['width'])
            height = float(row['height'])

            # Генерируем уникальный цвет для лодки
            if boat_id not in color_map:
                color_map[boat_id] = tuple(np.random.randint(0, 256, size=3).tolist())

            color = color_map[boat_id]
            center_position = (int(x + width / 2), int(y + height / 2))  # Преобразуем в int

            cv2.circle(image, center_position, 5, color, -1)

            if boat_id not in previous_positions:
                previous_positions[boat_id] = []
                
            previous_positions[boat_id].append(center_position)

            # Рисуем известные позиции с более толстыми линиями
            if len(previous_positions[boat_id]) > 1:
                for i in range(len(previous_positions[boat_id]) - 1):
                    cv2.line(image, previous_positions[boat_id][i], previous_positions[boat_id][i + 1], color, 4)  # Увеличиваем толщину линии

            # Предсказание будущих позиций
            future_positions = predict_future_positions(previous_positions[boat_id], steps=5)
            for i, pos in enumerate(future_positions):
                predicted_position = (int(pos[0]), int(pos[1]))
                cv2.circle(image, predicted_position, 5, (255, 0, 255), -1)  # Фиолетовые точки
                cv2.putText(image, f"{i + 1}s", (predicted_position[0]+5, predicted_position[1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        except Exception as e:
            print(f"Ошибка обработки строки {index}: {e}")
            continue

    cv2.imshow('Boat Positions', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Укажите пути к вашему изображению и CSV файлу
image_path = 'testVis.jpg'  # Путь к изображению
csv_path = 'test.csv'  # Путь к CSV-файлу

display_boat_positions(image_path, csv_path)