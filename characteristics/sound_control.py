
from bleak import BleakClient

from .abstract_characteristic import AbstractCharacteristic


class Sound(AbstractCharacteristic):
    """Sound characteristic.

        Args:
            name (str, optional): Name of toio. Defaults to None.
            client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        """Initialize the sound characteristic used in Toio.

        Args:
            name (str, optional): Name of toio. Defaults to None.
            client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
        """
        super().__init__(
            uuid='10b20104-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Sound Control',
            write=True,
            write_without_response=False,
            read=False,
            notify=False,
            name=name,
            client=client
        )

    async def play(
        self,
        sound_effect: int = 4,
        volume: int = 255
    ) -> None:
        write_value = bytearray(b'\x02')
        write_value.append(sound_effect)
        write_value.append(volume)

        await self._send_data(write_value)

    async def play_midi(
        self,
        repetition: int = 0,
        operation: int = 3,
        midi_note_numbers: list = [
            (30, 60, 255),
            (30, 62, 255),
            (30, 64, 255)
        ]
    ) -> None:
        write_value = bytearray(b'\x03')
        write_value.append(repetition)
        write_value.append(operation)
        for playback_time, midi_note_num, volume in midi_note_numbers:
            write_value.append(playback_time)
            write_value.append(midi_note_num)
            write_value.append(volume)

        await self._send_data(write_value)
