# -*- coding: utf-8 -*-

from typing import Dict

from bleak import BleakClient
from toio_API.utils.logging import initialize_logging

from toio_API.characteristics.abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Configuration(AbstractCharacteristic):
    """Configuration characteristic.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_configuration.

    Args:
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
            - Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid='10b201ff-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Configuration',
            write=True,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    async def request_information(self) -> None:
        write_value = bytearray(b'\x01')
        write_value.append(0)

        await self._send_data(write_value)

    async def set_level_threshold(self, threshold: int = 45) -> None:
        write_value = bytearray(b'\x05')
        write_value.append(0)
        write_value.append(threshold)

        await self._send_data(write_value)

    async def set_collision_threshold(self, threshold: int = 7) -> None:
        write_value = bytearray(b'\x06')
        write_value.append(0)
        write_value.append(threshold)

        await self._send_data(write_value)

    async def set_double_tap_interval(self, interval: int = 5) -> None:
        write_value = bytearray(b'\x17')
        write_value.append(0)
        write_value.append(interval)

        await self._send_data(write_value)

    async def set_reader_notification(self, minimum_interval: int = 1, condition: int = 255) -> None:
        write_value = bytearray(b'\x18')
        write_value.append(0)
        write_value.append(minimum_interval)
        write_value.append(condition)

        await self._send_data(write_value)

    async def set_reader_missed_notification(self, sensitivity: int = 7) -> None:
        write_value = bytearray(b'\x19')
        write_value.append(0)
        write_value.append(sensitivity)

        await self._send_data(write_value)

    async def enable_magnetic_sensor(self, turn_on: bool = False) -> None:
        write_value = bytearray(b'\x1b')
        write_value.append(0)
        write_value.append(1 if turn_on else 0)

        await self._send_data(write_value)

    async def enable_motor_speed_notification(self, turn_on: bool = False) -> None:
        write_value = bytearray(b'\x1c')
        write_value.append(0)
        write_value.append(1 if turn_on else 0)

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the configuration characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the configuration characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        if data[0] == int.from_bytes(bytearray(b'\x81'), 'little'):
            response = {
                'response_type': data[0],
                'reserved': data[1],
                'ble_protocol_version': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\x98'), 'little'):
            response = {
                'response_type': data[0],
                'reserved': data[1],
                'result': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\x99'), 'little'):
            response = {
                'response_type': data[0],
                'reserved': data[1],
                'result': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\x9b'), 'little'):
            response = {
                'response_type': data[0],
                'reserved': data[1],
                'result': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\x9c'), 'little'):
            response = {
                'response_type': data[0],
                'reserved': data[1],
                'result': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        else:
            logger.warn(f'[{self.name}] [{self.descriptor}] data[0]: {data[0]}')

            raise ValueError()
