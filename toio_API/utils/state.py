# -*- coding: utf-8 -*-

class State:
    """State to represent the property of characteristics.

    Args:
        write (bool, optional): Write property.
            - Defaults to False.
        write_without_response: Write without response property.
            - Defaults to False.
        read (bool, optional): Read property.
            - Defaults to False.
        notify (bool, optional): Notify property.
            - Defaults to False.
    """
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
    def write_without_response(self):
        return self.__write_without_response

    @property
    def read(self):
        return self.__read

    @property
    def notify(self):
        return self.__notify
