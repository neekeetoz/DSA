"""
Сервер
"""
import cv2
import socket

"""
Создание сервера:

Аргументы, передаваемые для socket() - указание семейства адресов и типа сокета

AF_INET - это семейство интернет-адресов для IPv4  

SOCK_STREAM - это тип сокета для TCP протокола, который будет использоваться для передачи наших сообщений в сети
"""
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

"""
Передаваемые значения bind() зависят от семейства адресов сокета. 

В данном примере мы используем socket.AF_INET(IPv4). Таким образом, ожидается 2-кортеж: (host, port).

"""
server.bind(("127.0.0.1", 1235))  # localhost

server.listen()  # может принимать некоторое количество сообщений
print("Сервер слушает", '\n')

# Ожидание подключения клиента
client_socket, client_address = server.accept()

"""
После получения объекта клиентского сокета client_socket из accept() 

бесконечный цикл while используется для блокировки вызовов client_socket.recv(). 

Это считывает любые данные, которые отправляет клиент, и возвращает их обратно, используя staging_server2.send().

Если client_socket.recv() возвращает пустой bytes объект, то клиент закрыл соединение и цикл завершился. 

Цикл while используется для client_socket автоматического закрытия сокета в конце блока.
"""
while True:
    try:
        data = client_socket.recv(2048)
        sizeOfImage = int(data.decode())
        print("Размер входного изображения:", sizeOfImage)

        # Принимаю картинку
        file = open('image_server.png', mode="wb")  # открыть для записи принимаемой картинки файл

        while sizeOfImage > 0:
            data = client_socket.recv(2048)
            file.write(data)
            sizeOfImage = sizeOfImage - 2048

        file.close()

        # Применение медианного фильтра
        image = cv2.imread('image_server.png')

        # применить медианный фильтр 49×49 к изображению
        processed_image = cv2.medianBlur(image, 49)

        # сохранить образ на диск
        cv2.imwrite('image_server_filter.png', processed_image)
        print("Изображение обработано", '\n')
    except:
        print("Произошла непредвиденная ошибка", '\n')
        break

server.close()
