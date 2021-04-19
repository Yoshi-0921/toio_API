
from bleak import BleakClient

from characteristics.abstract_characteristic import AbstractCharacteristic


class Lamp(AbstractCharacteristic):
    """Lamp characteristic.

    Args:
        name (str, optional): Name of toio. Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
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

    async def switch(
        self,
        time: int = 16,
        red: int = 255,
        green: int = 0,
        blue: int = 0
    ) -> None:
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
        time1: int = 30,
        red1: int = 0,
        green1: int = 255,
        blue1: int = 0,
        time2: int = 30,
        red2: int = 0,
        green2: int = 0,
        blue2: int = 255
    ) -> None:
        write_value = bytearray(b'\x04')
        write_value.append(repetition)
        write_value.append(operation)
        write_value.append(time1)
        write_value.append(1)
        write_value.append(1)
        write_value.append(red1)
        write_value.append(green1)
        write_value.append(blue1)
        write_value.append(time2)
        write_value.append(1)
        write_value.append(1)
        write_value.append(red2)
        write_value.append(green2)
        write_value.append(blue2)

        await self._send_data(write_value)

    async def turn_off_all(self) -> None:
        write_value = bytearray(b'\x01')

        await self._send_data(write_value)

    async def turn_off(self) -> None:
        write_value = bytearray(b'\x02')
        write_value.append(1)
        write_value.append(1)

        await self._send_data(write_value)
