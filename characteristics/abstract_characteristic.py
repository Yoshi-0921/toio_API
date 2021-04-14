
from abc import ABC, abstractclassmethod
from utils.property import Property


class AbstractCharacteristic(ABC):
    def __init__(
        self,
        uuid: str = None,
        descriptor: str = None,
        write: bool = False,
        read: bool = False,
        notify: bool = False,
    ):
        self.__uuid = uuid
        self.__descriptor = descriptor
        self.__property = Property(
            write=write,
            read=read,
            notify=notify
        )

    @property
    def uuid(self):
        return self.__uuid

    @property
    def descriptor(self):
        return self.__descriptor

    @property
    def property(self):
        return self.__property
