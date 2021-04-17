
from bleak import BleakClient
from utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class MotionSensor(AbstractCharacteristic):
    def __init__(self, name: str, client: BleakClient):
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

    async def request_information(self):
        write_value = bytearray(b'\x81')

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray):
        detection = {
            'detection_type': data[0],
            'level': data[1],
            'collision': data[2],
            'double_tap': data[3],
            'posture': data[4],
            'shake': data[5]
        }
        logger.info(f'[{self.name}] [{self.descriptor}] {detection}')

        return detection


class MagneticSensor(AbstractCharacteristic):
    def __init__(self, name: str, client: BleakClient):
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

    async def request_information(self):
        write_value = bytearray(b'\x82')

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray):
        detection = {
            'detection_type': data[0],
            'magnet_state': data[1],
        }
        logger.info(f'[{self.name}] [{self.descriptor}] {detection}')

        return detection
