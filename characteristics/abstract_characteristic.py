
from abc import ABC
from utils.state import State
from bleak import BleakClient


class AbstractCharacteristic(ABC):
    def __init__(
        self,
        uuid: str = None,
        descriptor: str = None,
        write: bool = False,
        write_without_response: bool = False,
        read: bool = False,
        notify: bool = False,
        client: BleakClient = None
    ):
        self.__uuid = uuid
        self.__descriptor = descriptor
        self.__state = State(
            write=write,
            write_without_response=write_without_response,
            read=read,
            notify=notify
        )
        self.__client = client

    @property
    def uuid(self):
        return self.__uuid

    @property
    def descriptor(self):
        return self.__descriptor

    @property
    def state(self):
        return self.__state

    @property
    def client(self):
        return self.__client
