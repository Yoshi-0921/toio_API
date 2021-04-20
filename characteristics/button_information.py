# -*- coding: utf-8 -*-

from typing import Dict

from bleak import BleakClient
from utils.logging import initialize_logging

from characteristics.abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Button(AbstractCharacteristic):
    """Button characteristic.

    Args:
        name (str, optional): Name of toio. Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid='10b20107-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Button Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the button characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the button characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        response = {
            'button_id': data[0],
            'button_state': data[1]
        }
        logger.info(f'[{self.name}] [{self.descriptor}] {response}')

        return response
