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

    time = 0
    timex = 0
    event = 0
    action_x = 0
    action_y = 0
    action = None
    admin = ""
    user_x = 0
    user_y = 0
    user = "SomeOne"
    u_x = 0
    u_y = 0
    userip = "0.0.0.0"

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
            self.lines = [line.rstrip() for line in self.lines]
            self.S("...Успешно")
            self.I("Подготовка '{}' для следующего цикла".format(self.WORKING))
            try:
                #open(self.WORKING, mode='w').close()
                self.S("...Успешно")
            except:
                self.E()

        except:
            self.E()

        self.I("Форматирование событий за последние 60 секунд:")

        chest = 0

        for event in range(int(len(self.lines))):
            if event != 0 and chest % 3 == 0:
                chest = chest + 1
                continue

            chest = 0
            checker = 0
            for i in range(len(self.lines[event])):
                check = self.lines[event][-i:]
                if i > 1:
                    check = check[:1]
                if check == ":":
                    self.SERVER = self.lines[event][:-i]

            for i in range(len(self.lines[event])):
                check = self.lines[event][-i:]
                if i > 1:
                    check = check[:1]
                if check == ":" and checker == 0:
                    self.u_x = i
                    checker = 1
                if check == "(":
                    self.admin = self.lines[event][len(self.SERVER)+2:-i]
                if check == "(" and checker == 1:
                    self.action_x = i
                    checker = 2
                if check == ")":
                    self.action_y = i
                if check == ";":
                    self.u_y = i
                if check == "{":
                    self.time = int(self.lines[event][len(self.lines[event])-i+1:-1:])
                    self.timex = i

            self.userip = self.lines[event][-self.u_x+1:-self.u_y:]
            self.action = self.lines[event][-self.action_y+2:-self.action_x-1:]
            server = self.SERVER
            suffix = "{} минут".format(self.time)
            if self.time >= 60:
                self.time = round(self.time/60)
                suffix = "{} час(а/ов)".format(self.time)
                if self.time >= 24:
                    self.time = round(self.time/24)
                    suffix = "{} день/дней".format(self.time)
                    if self.time >= 30:
                        self.time = round(self.time/30)
                        suffix ="{} месяц(ев)".format(self.time)
                        if self.time >= 12:
                            self.time = round(self.time/12)
                            suffix = "Пермамент ( {} лет/год(ов) )".format(self.time)

            import sender

            if self.action == "BAN":
                self.user = self.lines[event + 1][len(self.SERVER)+29:]
                if len(self.user) > 32:
                    self.W("Событие номер {} оказалось поврежденным".format(round(event/2)))
                    self.W("Пропуск")
                    continue
                self.I(self.admin+" забанил "+self.user+"("+self.userip+") на сервере "+server+" на "+suffix)
                sender.Send(self.ADRESS, [self.admin, self.user, self.userip, server, suffix, self.action])
            if self.action == "FORCECLASS":
                self.user = self.lines[event + 1][len(self.SERVER)+26:]
                if len(self.user) > 32:
                    self.W("Событие номер {} оказалось поврежденным".format(round(event/2)))
                    self.W("Пропуск")
                    continue
                self.I(self.admin + " выдал класс #" + str(self.time) + " игроку " + self.user + "("+self.userip+") на сервере " + server)
                sender.Send(self.ADRESS, [self.admin, self.user, self.userip, server, self.time, self.action])
            if self.action == "GIVE":
                self.user = self.lines[event + 1][len(self.SERVER)+17:]
                if len(self.user) > 32:
                    self.W("Событие номер {} оказалось поврежденным".format(round(event/2)))
                    self.W("Пропуск")
                    continue
                self.I(self.admin + " выдал предмет #" + str(self.time) + " игроку " + self.user + "("+self.userip+") на сервере " + server)
                sender.Send(self.ADRESS, [self.admin, self.user, self.userip, server, self.time, self.action])

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
