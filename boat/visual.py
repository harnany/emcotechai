import cv2
import pandas as pd

def display_boat_positions(image_path, csv_path):
    # Загружаем изображение
    image = cv2.imread(image_path)

    if image is None:
        print("Ошибка загрузки изображения.")
        return

    # Загружаем данные о лодках из CSV
    df = pd.read_csv(csv_path, sep=';')  # Убедитесь, что разделитель совпадает с вашим CSV

    for index, row in df.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        width = int(row['width'])
        height = int(row['height'])

        # Рисуем прямоугольник вокруг лодки
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
        cv2.putText(image, f'Boat {int(row["boat_id"])}', (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Отображаем изображение
    cv2.imshow('Boat Positions', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Укажите пути к вашему изображению и CSV-файлу
image_path = 'testVis.jpg'  # Путь к изображению
csv_path = 'test.csv'  # Путь к CSV-файлу

display_boat_positions(image_path, csv_path)