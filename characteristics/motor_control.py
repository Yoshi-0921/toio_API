
from .abstract_characteristic import AbstractCharacteristic


class Motor(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20102-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Motor Control',
            write=False,
            write_without_response=True,
            read=True,
            notify=True,
            client=client
        )

    async def control(
        self,
        left_forward: bool = True,
        left_speed: int = 100,
        right_forward: bool = False,
        right_speed: int = 20
    ):
        write_value = bytearray(b'\x01')
        write_value.append(1)
        write_value.append(1 if left_forward else 2)
        write_value.append(left_speed)
        write_value.append(2)
        write_value.append(1 if right_forward else 2)
        write_value.append(right_speed)

        await self.client.write_gatt_char(self.uuid, write_value)

    async def time_control(
        self,
        left_forward: bool = True,
        left_speed: int = 100,
        right_forward: bool = False,
        right_speed: int = 20,
        time: int = 10
    ):
        write_value = bytearray(b'\x02')
        write_value.append(1)
        write_value.append(1 if left_forward else 2)
        write_value.append(left_speed)
        write_value.append(2)
        write_value.append(1 if right_forward else 2)
        write_value.append(right_speed)
        write_value.append(time)

        await self.client.write_gatt_char(self.uuid, write_value)

    async def target_control(
        self,
        identifier: int = 0,
        time_out: int = 5,
        movement: int = 0,
        max_speed: int = 50,
        acceleration: int = 0,
        x_coordinate: int = 700,
        y_coordinate: int = 386,
        theta: int = 90
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
        write_value.extend(bytearray(b'\x00\x5a'))

        await self.client.write_gatt_char(self.uuid, write_value)

    async def targets_control(
        self,
        identifier: int = 0,
        time_out: int = 5,
        movement: int = 0,
        max_speed: int = 50,
        acceleration: int = 0,
        overwrite: int = 1,
        x1_coordinate: int = 100,
        y1_coordinate: int = 100,
        theta2: int = 0,
        x2_coordinate: int = 200,
        y2_coordinate: int = 100,
        theta1: int = 90,
        x3_coordinate: int = 200,
        y3_coordinate: int = 200,
        theta3: int = 180
    ):
        write_value = bytearray(b'\x04')
        write_value.append(identifier)
        write_value.append(time_out)
        write_value.append(movement)
        write_value.append(max_speed)
        write_value.append(acceleration)
        write_value.append(0)
        write_value.append(overwrite)
        write_value.extend(x1_coordinate.to_bytes(2, 'little'))
        write_value.extend(y1_coordinate.to_bytes(2, 'little'))
        write_value.extend(bytearray(b'\x00\x00'))
        write_value.extend(x2_coordinate.to_bytes(2, 'little'))
        write_value.extend(y2_coordinate.to_bytes(2, 'little'))
        write_value.extend(bytearray(b'\x5f\x00'))
        write_value.extend(x3_coordinate.to_bytes(2, 'little'))
        write_value.extend(y3_coordinate.to_bytes(2, 'little'))
        write_value.extend(bytearray(b'\xb4\x00'))

        await self.client.write_gatt_char(self.uuid, write_value)
