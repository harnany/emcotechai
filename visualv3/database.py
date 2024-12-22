import pandas as pd  # Импортируем библиотеку pandas для работы с данными

class BoatDatabase:
    def __init__(self, video_name):
        """
        Инициализация базы данных лодок.
        
        :param video_name: Имя видео для сохранения в файл
        """
        self.video_name = video_name  # Сохраняем имя видео
        self.coordinates = []  # Инициализация списка для хранения координат

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
        self.coordinates.append((boat_id, x, y, width, height, timestamp))  # Добавляем координаты в список

    def save_to_csv(self):
        """
        Сохраняет координаты лодок в CSV файл.
        """
        # Создаем DataFrame из списка координат с заданными заголовками
        df = pd.DataFrame(self.coordinates, columns=['boat_id', 'x', 'y', 'width', 'height', 'timestamp'])
        df.to_csv(f'{self.video_name}_coordinates.csv', sep=';', index=False)  # Сохраняем DataFrame в CSV с разделителем ';'
        print(f'Координаты сохранены в {self.video_name}_coordinates.csv')  # Информируем о завершении

# Пример использования:
# db = BoatDatabase(video_name='my_video')  # Создаем экземпляр базы данных с именем видео
# db.add_coordinate('Boat 1', 100, 150, 50, 20, 0.5)  # Добавление данных (пример)
# db.save_to_csv()  # Сохранение данных в CSV файл