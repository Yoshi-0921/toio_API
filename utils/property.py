
class Property:
    def __init__(
        self,
        write: bool = False,
        write_without_response: bool = False,
        read: bool = False,
        notify: bool = False
    ):
        self.__write = write
        self.__read = read
        self.__notify = notify

    @property
    def write(self):
        return self.__write

    @property
    def read(self):
        return self.__read

    @property
    def notify(self):
        return self.__notify
