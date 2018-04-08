import os

import writer
from time import *


class Filt(object):

    S = writer.Stream.success
    E = writer.Stream.error
    W = writer.Stream.warning
    I = writer.Stream.info

    WORKING = ""
    SERVER = ""

    EVENTS = []
    MULTIACTION = False;

    time = 0
    event = 0
    action = None
    admin = ""
    multiuser = []
    multiuserip = []

    def __init__(self, directory, adress):

        self.DIRECTORY = directory
        self.ADRESS = adress
        self.check()
        while True:
            self.prepare()
            sleep(60) # Cool down before each check

    ###

    def prepare(self):
        self.W("Подготовка пакетов к отправке...")
        self.I("Удаление мусора из {}".format(self.WORKING))
        try:
            self.lines = open(self.WORKING, mode='r', encoding='UTF-8').readlines()
            self.lines = [line.strip("\n") for line in self.lines]
            self.S("...Успешно")
            self.I("Подготовка '{}' для следующего цикла".format(self.WORKING))
            try:
                open(self.WORKING, mode='w').close()
                self.S("...Успешно")
            except:
                self.E()

        except:
            self.E()

        self.I("Форматирование событий за последние 60 секунд:")

        chest = 0

        for event in range(int(len(self.lines))):
            if self.lines[event][-2:] == "`%":
                continue

            self.multiuser = []
            self.multiuserip = []
            self.time = 0
            self.event = 0
            self.action = None
            self.admin = ""

            # Макет действий
            # SCPSL Community Keter 1: Italian Man Who went to Malta(::ffff:188.168.4.16) FORCECLASS (::ffff:80.253.235.21; ::ffff:46.188.125.52; ::ffff:95.32.34.206; ::ffff:46.219.212.194; ::ffff:178.70.136.112; ::ffff:2.94.255.176; ) {1}
            # SCPSL Community Keter 1: forced class applied to Alex_STALKER1221
            # SCPSL Community Keter 1: forced class applied to БУНД БЛЯТЬ
            # SCPSL Community Keter 1: forced class applied to Zett
            # SCPSL Community Keter 1: forced class applied to DOCtor
            # SCPSL Community Keter 1: forced class applied to Lonwrat
            # SCPSL Community Keter 1: forced class applied to ... а что Титов?

            # Определение сервера
            self.SERVER = self.lines[event].split(":")[0]
            # Определение действия
            self.action = self.lines[event].\
                split("::ffff:")[1].split(") ")[1].split(" (")[0]
            # Определение админа
            self.admin = self.lines[event].split(": ")[1].split("(::")[0]
            # Определение IP целей
            self.multiuserip = self.lines[event].split("(")[2].split(" )")[0].split(";")
            # Отброс мусора в виде ::ffff:
            for garbage in range(len(self.multiuserip)):
                self.multiuserip[garbage] = self.multiuserip[garbage].strip("::ffff:").strip(" ")
            # Определение аргумента
            self.time = self.lines[event].split("; ) {")[1].split("}")[0]
            # Определение целей
            skip = 1
            while True:
                try:
                    if self.lines[event + skip][-2:] == "`%":
                        self.multiuser.append(self.lines[event + skip].split(" to ")[1].strip("`%"))
                        skip += 1
                    else:
                        break
                except:
                    break

            import sender
            # Определение количества событий за один момент
            # Если конечно, такие есть

            # Определение пропуска для +1 линии и маски отправки
            addition = 0
            mask = ""
            if self.action == "BAN":
                addition = 27
                mask = "{} забанил игрока {}({}) на сервере {} время бана {}"
                suffix = "{} минут".format(self.time)
                # Определение времени
                self.time = int(self.time)
                if self.time >= 60:
                    self.time = round(self.time / 60)
                    suffix = "{} час(а/ов)".format(self.time)
                    if self.time >= 24:
                        self.time = round(self.time / 24)
                        suffix = "{} день/дней".format(self.time)
                        if self.time >= 30:
                            self.time = round(self.time / 30)
                            suffix = "{} месяц(ев)".format(self.time)
                            if self.time >= 12:
                                self.time = round(self.time / 12)
                                suffix = "Пермамент ( {} лет/год(ов) )".format(self.time)
                self.time = suffix
            elif self.action == "FORCECLASS":
                addition = 24
                mask = "{} выдал класс {} игроку {}({}) на сервере {}"
            elif self.action == "GIVE":
                addition = 15
                mask = "{} выдал предмет {} игроку {}({}) на сервере {}"

            # Отправление информации по сокету
            for item in range(len(self.multiuser)):
                if self.action == "BAN":
                    self.I(mask.format(self.admin, self.multiuser[item], self.multiuserip[item], self.SERVER, self.time))
                else:
                    self.I(mask.format(self.admin, self.time, self.multiuser[item], self.multiuserip[item], self.SERVER))
                sender.Send(self.ADRESS, [self.admin, self.multiuser[item], self.multiuserip[item], self.SERVER, self.time, self.action])

            sleep(0.5)
            self.event = self.event + 1

        self.S("Количество событий за последние 60 секунд: {}\n".format(self.event))
        if self.event != 0:
            self.S("Проверьте #prison-list на наличие результата")
            self.W("Если результата не будет в течении 5-ти минут, обращайтесь к RED x AK GOD\n")

    ###

    def check(self):
        try:
            files = os.listdir(self.DIRECTORY)
        except:
            self.E("Папка логов пуста или не существует")
            self.E("Исправьте ошибку")
            self.E()

        self.S("Папка подлинна")
        sleep(0.5)
        for file in range(len(files)):
            try:
                sleep(0.5)
                if files[file][-25:] == "_MODERATOR_output_log.txt":
                    self.S("Найден административный Лог файл - {} ".format(files[file]))
                    self.WORKING = self.DIRECTORY + "/" + files[file]

                elif files[file][-19:] == "_SCP_output_log.txt":
                    self.I("Найден SCP Лог файл - {}".format(files[file]))
                elif files[file][-18:] == "_MA_output_log.txt":
                    self.I("Найден MA Лог файл - {}".format(files[file]))
                else:
                    self.removeyn(files[file])
            except:
                self.removeyn(files[file])

        if len(self.WORKING) == 0:
            self.E("Не было найдено ни однго административного файла. При появлении, перезапустите", True)

    ###

    def removeyn(self, file):

        self.W("Найден файл который не удалось отсортировать")

        while True:
            self.W("Удалить? '{}' (Y/N)".format(file))
            YN = input()
            if YN == "Y" or YN == "y":

                try:
                    os.remove(self.DIRECTORY + "/" + file)
                    self.S("Файл был успешно удален")
                    break

                except:
                    try:
                        os.rmdir(self.DIRECTORY + "/" + file)
                        self.S("Папка была успешно удалена")
                        break
                    except:
                        self.E("Не удалось удалить файл. Файл будет оставлен")
                        break

            elif YN == "N" or YN == "n":
                self.I("Файл не был удален")
                break

            else:
                pass

