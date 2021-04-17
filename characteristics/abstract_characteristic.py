
from abc import ABC

from bleak import BleakClient
from utils.logging import initialize_logging
from utils.state import State

logger = initialize_logging(__name__)


class AbstractCharacteristic(ABC):
    def __init__(
        self,
        uuid: str = None,
        descriptor: str = None,
        write: bool = False,
        write_without_response: bool = False,
        read: bool = False,
        notify: bool = False,
        name: str = None,
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
        self.__name = name
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
    def name(self):
        return self.__name

    @property
    def client(self):
        return self.__client

    async def start_notify(self):
        await self.__client.start_notify(self.__uuid, self._notification_callback)

    async def stop_notify(self):
        await self.__client.stop_notify(self.__uuid)

    async def get_information(self):
        try:
            raw_response = await self.__client.read_gatt_char(self.__uuid)
            response = self._notification_callback(0, raw_response)
            return response

        except AttributeError:
            logger.info(f'[{self.__name}] [{self.__descriptor}] Attribute Error occured when receiving data.')

    def _notification_callback(self, sender: int, data: bytearray):
        raise NotImplementedError()

    async def _send_data(self, write_value: bytearray):
        try:
            await self.__client.write_gatt_char(self.__uuid, write_value)

        except AttributeError:
            logger.info(f'[{self.__name}] [{self.__descriptor}] Attribute Error occured when sending data.')
