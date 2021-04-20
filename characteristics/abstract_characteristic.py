# -*- coding: utf-8 -*-

from abc import ABC
from typing import Dict

from bleak import BleakClient
from utils.logging import initialize_logging
from utils.state import State

logger = initialize_logging(__name__)


class AbstractCharacteristic(ABC):
    """Abstract class of characteristics used in Toio.

    Args:
        uuid (str, optional): UUID of the characteristic.
            - Defaults to None.
        descriptor (str, optional): Description of the characteristic.
            - Defaults to None.
        write (bool, optional): Write property.
            - Defaults to False.
        write_without_response: Write without response property.
            - Defaults to False.
        read (bool, optional): Read property.
            - Defaults to False.
        notify (bool, optional): Notify property.
            - Defaults to False.
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
            - Defaults to None.
    """
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
    ) -> None:
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
    def uuid(self) -> str:
        return self.__uuid

    @property
    def descriptor(self) -> str:
        return self.__descriptor

    @property
    def state(self) -> State:
        return self.__state

    @property
    def name(self) -> str:
        return self.__name

    @property
    def client(self) -> BleakClient:
        return self.__client

    async def start_notify(self) -> None:
        """Starts notification of the characteristics.
        """
        await self.__client.start_notify(self.__uuid, self._notification_callback)

    async def stop_notify(self) -> None:
        """Stops notification of the characteristics.
        """
        await self.__client.stop_notify(self.__uuid)

    async def read_information(self) -> Dict[str, int]:
        """Reads information obtained by the characteristics.

        Returns:
            Dict[str, int]: Decoded response from the characteristics.
        """
        try:
            raw_response = await self.__client.read_gatt_char(self.__uuid)
            response = self._notification_callback(0, raw_response)
            return response

        except AttributeError:
            logger.exception(f'[{self.__name}] [{self.__descriptor}] Attribute Error occured when receiving data.')

    def _notification_callback(self, sender: int, data: bytearray) -> Dict[str, int]:
        """Abstract method to decode binary notification.

        Args:
            sender (int): Sender that sends the data.
            data (bytearray): Sent binary data.

        Raises:
            NotImplementedError: Implement this code if required in certain characteristics.

        Returns:
            Dict[str, int]: Decoded response from the characteristics.
        """
        raise NotImplementedError()

    async def _send_data(self, write_value: bytearray) -> None:
        """Sends bytearray data to the BleakClient via BLE connection.

        Args:
            write_value (bytearray): Binary data to send.
        """
        try:
            await self.__client.write_gatt_char(self.__uuid, write_value)

        except AttributeError:
            logger.exception(f'[{self.__name}] [{self.__descriptor}] Attribute Error occured when sending data.')
