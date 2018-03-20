import time
import socket
from writer import *


class Send(object):

    def __init__(self, ADRESS, array = None):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                try:
                    s.connect((ADRESS, 3000))
                except:
                    Stream.error(self, msg="Не удалось подключится... Перезапуск через 2 секунды")
                    time.sleep(2)
                    continue
                string = "%' "
                try:
                    for item in range(len(array)):
                            string = string + str(array[item])
                            if item != len(array)-1:
                                string = string + ","
                except:
                    Stream.error(self, msg="Не удалось конвертировать в байты. Пропуск")
                    break
                s.sendall(bytes(string.encode()))
                data = s.recv(1024)
                if data:
                    Stream.success(self, msg="Пакет успешно доставлен")
                break

