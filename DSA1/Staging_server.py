"""
Промежуточный Сервер
"""

import socket
import time
import cv2
import numpy as np
import os

"""
Создание промежуточного сервера:

Аргументы, передаваемые для socket() - указание семейства адресов и типа сокета

AF_INET - это семейство интернет-адресов для IPv4  

SOCK_STREAM - это тип сокета для TCP протокола, который будет использоваться для передачи наших сообщений в сети
"""
staging_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

"""
Передаваемые значения bind() зависят от семейства адресов сокета. 

В данном примере мы используем socket.AF_INET(IPv4). Таким образом, ожидается 2-кортеж: (host, port).

"""
staging_server.bind(("127.0.0.1", 1234))  # localhost


#listen() разрешает серверу accept() подключаться

staging_server.listen()  # может принимать некоторое количество сообщений
print("Сервер слушает", '\n')

# Создание сервера для выходного изображения
staging_server2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

staging_server2.connect(("127.0.0.1", 1235))

"""
После получения объекта клиентского сокета client_socket из accept()  

бесконечный цикл while используется для блокировки вызовов client_socket.recv(). 

Это считывает любые данные, которые отправляет клиент, и возвращает их обратно, используя staging_server2.send().

Если client_socket.recv() возвращает пустой bytes объект, то клиент закрыл соединение и цикл завершился. 

Цикл while используется для client_socket автоматического закрытия сокета в конце блока.
"""
while True:
    try:
        # Ожидание подключения клиента
        client_socket, client_address = staging_server.accept()

        data1 = client_socket.recv(2048)
        sizeOfImage1 = int(data1.decode())
        print("Размер входного изображения:", sizeOfImage1)

        # Принимаю картинку
        file = open('image_staging_server.png', mode="wb")  # открыть для записи принимаемой картинки файл

        while sizeOfImage1 > 0:
            data = client_socket.recv(2048)
            file.write(data)
            sizeOfImage1 = sizeOfImage1 - 2048

        file.close()

        # Внесение шума
        image = cv2.imread('image_staging_server.png')
        row, col, ch = image.shape
        mean = 0
        var = 100
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = image + gauss

        # сохранить дешумированное изображение
        cv2.imwrite('image_staging_server_output.png', noisy)

        # считывает, отправляет размер и саму картинку
        file = open('image_staging_server_output.png', mode="rb")  # считываем картинку

        imageSize = os.path.getsize('image_staging_server_output.png')
        print("Размер выходного изображения:", imageSize)
        staging_server2.send(str(imageSize).encode())
        time.sleep(0.1)

        while imageSize > 0:
            data = file.read(2048)
            staging_server2.send(data)
            imageSize = imageSize - 2048

        file.close()
        print("Изображение отправлено", '\n')
    except:
        print("Произошла непредвиденная ошибка", '\n')
        break

staging_server.close()
