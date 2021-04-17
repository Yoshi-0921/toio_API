
from .abstract_characteristic import AbstractCharacteristic


class Sound(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20104-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Sound Control',
            write=True,
            write_without_response=False,
            read=False,
            notify=False,
            client=client
        )

    async def play(
        self,
        sound_effect: int = 4,
        volume: int = 255
    ):
        write_value = bytearray(b'\x02')
        write_value.append(sound_effect)
        write_value.append(volume)

        await self._send_data(write_value)
