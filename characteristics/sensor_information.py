
from typing import Dict

from bleak import BleakClient
from utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class MotionSensor(AbstractCharacteristic):
    """MotionSensor characteristic.

    Args:
        name (str, optional): Name of toio. Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid='10b20106-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Sensor Information',
            write=True,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    async def request_information(self) -> None:
        write_value = bytearray(b'\x81')

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the motion sensor characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the motion sensor characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        response = {
            'response_type': data[0],
            'level': data[1],
            'collision': data[2],
            'double_tap': data[3],
            'posture': data[4],
            'shake': data[5]
        }
        logger.info(f'[{self.name}] [{self.descriptor}] {response}')

        return response


class MagneticSensor(AbstractCharacteristic):
    """MagneticSensor characteristic.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        """Initialize the magnetic sensor characteristic used in Toio.

        Args:
            name (str, optional): Name of toio. Defaults to None.
            client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
        """
        super().__init__(
            uuid='10b20106-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Sensor Information',
            write=True,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    async def request_information(self) -> None:
        write_value = bytearray(b'\x82')

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the magnetic sensor characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the magnetic sensor characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        response = {
            'response_type': data[0],
            'magnet_state': data[1],
        }
        logger.info(f'[{self.name}] [{self.descriptor}] {response}')

        return response
