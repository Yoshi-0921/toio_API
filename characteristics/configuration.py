
from bleak import BleakClient
from utils.logging import initialize_logging

from characteristics.abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Configuration(AbstractCharacteristic):
    def __init__(self, name: str, client: BleakClient):
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

    async def request_information(self):
        write_value = bytearray(b'\x01')
        write_value.append(0)

        await self._send_data(write_value)

    async def set_level_threshold(self, threshold: int = 45):
        write_value = bytearray(b'\x05')
        write_value.append(0)
        write_value.append(threshold)

        await self._send_data(write_value)

    async def set_collision_threshold(self, threshold: int = 7):
        write_value = bytearray(b'\x06')
        write_value.append(0)
        write_value.append(threshold)

        await self._send_data(write_value)

    async def set_double_tap_interval(self, interval: int = 5):
        write_value = bytearray(b'\x17')
        write_value.append(0)
        write_value.append(interval)

        await self._send_data(write_value)

    async def set_reader_notification(self, minimum_interval: int = 1, condition: int = 255):
        write_value = bytearray(b'\x18')
        write_value.append(0)
        write_value.append(minimum_interval)
        write_value.append(condition)

        await self._send_data(write_value)

    async def set_reader_missed_notification(self, sensitivity: int = 7):
        write_value = bytearray(b'\x19')
        write_value.append(0)
        write_value.append(sensitivity)

        await self._send_data(write_value)

    async def enable_magnetic_sensor(self, turn_on: bool = False):
        write_value = bytearray(b'\x1b')
        write_value.append(0)
        write_value.append(1 if turn_on else 0)

        await self._send_data(write_value)

    async def enable_motor_speed_notification(self, turn_on: bool = False):
        write_value = bytearray(b'\x1c')
        write_value.append(0)
        write_value.append(1 if turn_on else 0)

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
