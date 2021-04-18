
from bleak import BleakClient
from utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Motor(AbstractCharacteristic):
    def __init__(self, name: str, client: BleakClient):
        super().__init__(
            uuid='10b20102-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Motor Control',
            write=False,
            write_without_response=True,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    async def control(
        self,
        left_speed: int = 100,
        right_speed: int = 20
    ):
        write_value = bytearray(b'\x01')
        write_value.append(1)
        write_value.append(1 if 0 <= left_speed else 2)
        write_value.append(abs(left_speed))
        write_value.append(2)
        write_value.append(1 if 0 <= right_speed else 2)
        write_value.append(abs(right_speed))

        await self._send_data(write_value)

    async def time_control(
        self,
        left_speed: int = 100,
        right_speed: int = 20,
        time: int = 10
    ):
        write_value = bytearray(b'\x02')
        write_value.append(1)
        write_value.append(1 if 0 <= left_speed else 2)
        write_value.append(abs(left_speed))
        write_value.append(2)
        write_value.append(1 if 0 <= right_speed else 2)
        write_value.append(abs(right_speed))
        write_value.append(time)

        await self._send_data(write_value)

    async def target_control(
        self,
        identifier: int = 0,
        time_out: int = 5,
        movement: int = 0,
        max_speed: int = 50,
        acceleration: int = 0,
        x_coordinate: int = 700,
        y_coordinate: int = 386,
        theta: int = 90,
        theta_type: int = 0,
    ):
        write_value = bytearray(b'\x03')
        write_value.append(identifier)
        write_value.append(time_out)
        write_value.append(movement)
        write_value.append(max_speed)
        write_value.append(acceleration)
        write_value.append(0)
        write_value.extend(x_coordinate.to_bytes(2, 'little'))
        write_value.extend(y_coordinate.to_bytes(2, 'little'))
        theta += (2 ** 13) * theta_type
        write_value.extend(theta.to_bytes(2, 'little'))

        await self._send_data(write_value)

    async def targets_control(
        self,
        identifier: int = 0,
        time_out: int = 5,
        movement: int = 0,
        max_speed: int = 50,
        acceleration: int = 0,
        overwrite: int = 1,
        coordinates_thetas: list = [
            (100, 100, 0, 0),
            (200, 100, 90, 0),
            (200, 200, 180, 0)
        ]
    ):
        if 29 < len(coordinates_thetas):
            logger.warn(f'[{self.name}] [{self.descriptor}] len(coordinates_thetas): {len(coordinates_thetas)}')

            raise ValueError()

        write_value = bytearray(b'\x04')
        write_value.append(identifier)
        write_value.append(time_out)
        write_value.append(movement)
        write_value.append(max_speed)
        write_value.append(acceleration)
        write_value.append(0)
        write_value.append(overwrite)
        for x_coordinate, y_coordinate, theta, theta_type in coordinates_thetas:
            write_value.extend(x_coordinate.to_bytes(2, 'little'))
            write_value.extend(y_coordinate.to_bytes(2, 'little'))
            write_value.extend(bytearray(b'\x00\x00'))
            theta += (2 ** 13) * theta_type
            write_value.extend(theta.to_bytes(2, 'little'))

        await self._send_data(write_value)

    async def acceleration_control(
        self,
        translation_speed: int = 50,
        acceleration: int = 5,
        rotation_speed: int = 15,
        rotation_direction: int = 0,
        cube_direction: int = 0,
        priority: int = 0,
        time: int = 100
    ):
        write_value = bytearray(b'\x05')
        write_value.append(translation_speed)
        write_value.append(acceleration)
        write_value.extend(rotation_speed.to_bytes(2, 'little'))
        write_value.append(rotation_direction)
        write_value.append(cube_direction)
        write_value.append(priority)
        write_value.append(time)

        await self._send_data(write_value)

    def _notification_callback(self, _: int, data: bytearray):
        if data[0] == int.from_bytes(bytearray(b'\x83'), 'little'):
            response = {
                'response_type': data[0],
                'identifier': data[1],
                'content': data[2]
            }
            logger.warn(f'[{self.name}] [{self.descriptor}] {response}')
            return response

        elif data[0] == int.from_bytes(bytearray(b'\x84'), 'little'):
            response = {
                'response_type': data[0],
                'identifier': data[1],
                'content': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        elif data[0] == int.from_bytes(bytearray(b'\xe0'), 'little'):
            response = {
                'response_type': data[0],
                'left_speed': data[1],
                'right_speed': data[2]
            }
            logger.info(f'[{self.name}] [{self.descriptor}] {response}')

            return response

        else:
            logger.warn(f'[{self.name}] [{self.descriptor}] data[0]: {data[0]}')

            raise ValueError()
