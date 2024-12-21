import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# Настройки
num_boats = 3
num_points = 10

# Начальные параметры для лодок
boat_ids = [1, 2, 3]  # Идентификаторы лодок
initial_positions = [
    (100, 150),  # Лодка 1
    (200, 250),  # Лодка 2
    (300, 100)   # Лодка 3
]
widths = [5, 6, 7]  # Ширины лодок
heights = [2, 3, 2]  # Высоты лодок

# Список для хранения данных
data = []

# Начальное время
start_time = datetime.now()

for i, (boat_id, (x_start, y_start), width, height) in enumerate(zip(boat_ids, initial_positions, widths, heights)):
    # Генерация траектории
    x = np.linspace(x_start, x_start + random.randint(50, 150), num_points) + np.random.normal(0, 5, num_points)
    y = np.linspace(y_start, y_start + random.randint(-50, 50), num_points) + np.random.normal(0, 5, num_points)

    # Генерация временных меток
    timestamps = [start_time + timedelta(seconds=i) for i in range(num_points)]

    # Добавляем данные в список
    for j in range(num_points):
        data.append((boat_id, x[j], y[j], width, height, timestamps[j].isoformat()))

# Создание DataFrame с данными
df = pd.DataFrame(data, columns=['boat_id', 'x', 'y', 'width', 'height', 'timestamp'])

# Сохранение данных в файл test.SVS с разделителем ';'
df.to_csv('test.csv', sep=';', index=False)

print("Данные сохранены в test.csv")