"""
Реализация socket клиент-сервер, передача сообщения
Клиент
"""
import os
import time
import socket
"""
Создание клиента:

Аргументы, передаваемые для socket() - указание семейства адресов и типа сокета

AF_INET - это семейство интернет-адресов для IPv4  

SOCK_STREAM - это тип сокета для TCP протокола, который будет использоваться для передачи наших сообщений в сети
"""
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("127.0.0.1", 1234))

# считывает и отправляет картинку
file = open('image.png', mode="rb")  # считываем картинку

# определяем размер изображения
imageSize = os.path.getsize('image.png')
print("Размер изображения:", imageSize)

# Он создает объект сокета, подключается к серверу и вызывает staging_server2.send() отправку своего сообщения. 
# Наконец, он вызывает, client_socket.recv() чтобы прочитать ответ сервера, а затем распечатывает его.
client.send(str(imageSize).encode())
time.sleep(0.1)

while imageSize > 0:
    data = file.read(2048)
    client.send(data)
    imageSize = imageSize - 2048

print("Изображение отправлено")
file.close()
client.close()





