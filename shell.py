import os

import filtor
import sender
import writer


class Shell(object):

    success = writer.Stream.success
    error = writer.Stream.error
    warning = writer.Stream.warning
    info = writer.Stream.info

    WORKING = None
    ADRESS = None

    def __init__(self):

        self.SEND = sender.Send
        self.FILT = filtor.Filt

        self.clearconfig()
        filtor.sleep(2)

        #Настройка
        self.info("Настройка согласно конфигу...")
        try:
            filtor.sleep(0.5)
            lines = self.lines
            self.WORKING = lines[1]
            self.success("Рабочая директория: {}".format(self.WORKING))
            filtor.sleep(0.5)
            self.ADRESS = lines[3]
            self.success("Адресс JavaScript бота: {}".format(self.ADRESS))
            filtor.sleep(0.5)
            self.SERVERNAME = lines[5]
            self.success("Имя сервера: {}".format(self.SERVERNAME))
        except:
            self.error()


        self.checkconnection()
        self.logcheck()

    def checkconnection(self):
        # Проверка соеденения с JS ботом

        self.info("Настройка завершена")
        self.info("Проверка соеденения с ботом...")
        filtor.sleep(1)
        try:
            # self.SEND(self.ADRESS)
            self.success("Подключенно к {}".format(self.ADRESS))
        except:
            self.error("Не удалось подключится к {}".format(self.ADRESS))
            self.error()

    def logcheck(self):
        # Проверка на логи

        self.info("Проверка на наличие логов")
        filtor.sleep(0.5)
        self.info("При успехе, начало работы программы")
        filtor.sleep(0.5)
        self.FILT(self.WORKING, self.SERVERNAME, self.ADRESS)


    def clearconfig(self):
        # Чистка файла от мусора
        self.info("Очистка config.cfg от мусора...")
        filtor.sleep(0.5)
        try:
            bomfix = open(os.path.dirname(__file__) + '/../config.cfg', mode='r', encoding='utf-8-sig').read()
            open(os.path.dirname(__file__) + '/../config.cfg', mode='w', encoding='utf-8').write(bomfix)
            self.success("BOM Символ удален")
        except:
            self.error()
        filtor.sleep(0.5)
        try:
            self.lines = open(os.path.dirname(__file__) + '/../config.cfg', mode='r').readlines()
            self.lines = [line.rstrip() for line in self.lines]

            self.success("NEWLINE Символы удалены")
        except:
            self.error()


Shell()
input("Конец программы...\nНажмите ENTER для выхода...")
