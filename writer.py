import sys

class Stream:

    def error(self, msg = None, stop = None):
        if msg is not None:
            print("[ERROR]: {}".format(msg))
            if stop is not None:
                input("Конец программы...\nНажмите ENTER для выхода...")
                exit()
        else:
            print("[ERROR]: {}".format(sys.exc_info()[1]))
            input("Конец программы...\nНажмите ENTER для выхода...")
            exit()

    def warning(self, msg):
        print("[WARNING]: {}".format(msg))

    def info(self, msg):
        print("[INFO]: {}".format(msg))

    def success(self, msg):
        print("[SUCCESS]: {}".format(msg))