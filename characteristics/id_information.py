# -*- coding: utf-8 -*-

from typing import Dict

from bleak import BleakClient
from utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Reader(AbstractCharacteristic):
    """Reader characteristic.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_id.

    Args:
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
            - Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid='10b20101-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='ID Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the reader characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the reader characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        if data[0] == int.from_bytes(bytearray(b'\x01'), 'little'):
            response = {
                'response_type': data[0],
                'center_x': int.from_bytes(data[1:3], 'little'),
                'center_y': int.from_bytes(data[3:5], 'little'),
                'center_theta': int.from_bytes(data[5:7], 'little'),
                'sensor_x': int.from_bytes(data[7:9], 'little'),
                'sensor_y': int.from_bytes(data[9:11], 'little'),
                'sensor_theta': int.from_bytes(data[11:13], 'little')
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\x02'), 'little'):
            response = {
                'response_type': data[0],
                'standard_id': int.from_bytes(data[1:5], 'little'),
                'cube_theta': int.from_bytes(data[5:7], 'little')
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\x03'), 'little'):
            logger.warn(f'[{self.name}] [{self.descriptor}] Position ID missed.')

            return

        elif data[0] == int.from_bytes(bytearray(b'\x04'), 'little'):
            logger.warn(f'[{self.name}] [{self.descriptor}] Standard ID missed.')

            return

        else:
            logger.warn(f'[{self.name}] [{self.descriptor}] data[0]: {data[0]}')

            raise ValueError()
