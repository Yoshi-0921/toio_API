# -*- coding: utf-8 -*-

from typing import List

from bleak import BleakClient

from characteristics.abstract_characteristic import AbstractCharacteristic


class Lamp(AbstractCharacteristic):
    """Lamp characteristic.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_light.

    Args:
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
         - Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid='10b20103-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Light Control',
            write=True,
            write_without_response=False,
            read=False,
            notify=False,
            name=name,
            client=client
        )

    async def turn_on(
        self,
        time: int = 16,
        red: int = 255,
        green: int = 0,
        blue: int = 0
    ) -> None:
        """Turns on the light of toio for a certain time.

        Args:
            time (int, optional): Time (*10 ms) to control the motors.
                - Set it in [0, 255] and 0 is exceptionally infinite.
                - Defaults to 16.
            red (int, optional): Intensity of red element of light source.
                - Set it in [0, 255] and 0 for turning off.
                - Defaults to 255.
            green (int, optional): Intensity of green element of light source.
                - Set it in [0, 255] and 0 for turning off.
                - Defaults to 0.
            blue (int, optional): Intensity of blue element of light source.
                - Set it in [0, 255] and 0 for turning off.
                - Defaults to 0.
        """
        write_value = bytearray(b'\x03')
        write_value.append(time)
        write_value.append(1)
        write_value.append(1)
        write_value.append(red)
        write_value.append(green)
        write_value.append(blue)

        await self._send_data(write_value)

    async def consecutive_switch(
        self,
        repetition: int = 0,
        operation: int = 2,
        time_rgbs: List[int, int, int, int] = [
            (30, 0, 255, 0),
            (30, 0, 0, 255)
        ]
    ) -> None:
        """Turns on the light for a certain time consequtively.

        Args:
            repetition (int, optional): How many times to repeat the light emission.
                - Set it in [0, 255] and 0 is exceptionally infinite.
                - Defaults to 0.
            operation (int, optional): The number of operations.
                - Set it in [1, 29].
                - Defaults to 2.
            time_rgbs (List[int, int, int, int], optional): Time, red, gree, and blue light of consequtive operations.
                - The element should be a tuple of (time, red, gree, blue).
                - The values of element should follow the same rule as those of turn_on method.
                - Defaults to [(30, 0, 255, 0), (30, 0, 0, 255)].
        """
        write_value = bytearray(b'\x04')
        write_value.append(repetition)
        write_value.append(operation)
        for time, red, green, blue in time_rgbs:
            write_value.append(time)
            write_value.append(1)
            write_value.append(1)
            write_value.append(red)
            write_value.append(green)
            write_value.append(blue)

        await self._send_data(write_value)

    async def turn_off(self) -> None:
        """Turns off the light of toio.
        """
        write_value = bytearray(b'\x01')

        await self._send_data(write_value)

