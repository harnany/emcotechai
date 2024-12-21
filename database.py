import pandas as pd

class BoatDatabase:
    def __init__(self, video_name):
        self.video_name = video_name
        self.coordinates = []

    def add_coordinate(self, boat_id, x, y, width, height, timestamp):
        """
        Добавляет координаты лодки в базу данных.
        
        :param boat_id: Идентификатор лодки
        :param x: Координата X
        :param y: Координата Y
        :param width: Ширина лодки
        :param height: Высота лодки
        :param timestamp: Временная метка (время в секундах)
        """
        self.coordinates.append((boat_id, x, y, width, height, timestamp))

    def save_to_csv(self):
        """
        Сохраняет координаты лодок в CSV файл.
        """
        df = pd.DataFrame(self.coordinates, columns=['Boat', 'X', 'Y', 'Width', 'Height', 'Time'])
        df.to_csv(f'{self.video_name}_coordinates.csv', index=False)
        print(f'Координаты сохранены в {self.video_name}_coordinates.csv')

# Пример использования:
# db = BoatDatabase(video_name='my_video')
# db.add_coordinate('Boat 1', 100, 150, 50, 20, 0.5)  # Добавление данных
# db.save_to_csv()  # Сохранение данных