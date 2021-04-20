# -*- coding: utf-8 -*-

from typing import List

from bleak import BleakClient

from .abstract_characteristic import AbstractCharacteristic


class Sound(AbstractCharacteristic):
    """Sound characteristic.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_sound.

    Args:
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
            - Defaults to None.
    """
    def __init__(self, name: str = None, client: BleakClient = None) -> None:
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

    async def stop(self):
        """Stops the sound of toio.
        """
        write_value = bytearray(b'\x01')

        await self._send_data(write_value)

    async def play(
        self,
        sound_effect: int = 4,
        volume: int = 255
    ) -> None:
        """Plays the sound effect at desired sound volume.

        Args:
            sound_effect (int, optional): Sound effect ID in [0, 10].
                - Set it 0 for enter.
                - Set it 1 for selected.
                - Set it 2 for cancel.
                - Set it 3 for cursor.
                - Set it 4 for mat in.
                - Set it 5 for mat out.
                - Set it 6 for get 1.
                - Set it 7 for get 2.
                - Set it 8 for get 3.
                - Set it 9 for effect 1.
                - Set it 10 for effect 2.
                - Defaults to 4.
            volume (int, optional): Volume of sound.
                - Set it in [0, 255] and 0 for no sound.
                - Defaults to 255.
        """
        write_value = bytearray(b'\x02')
        write_value.append(sound_effect)
        write_value.append(volume)

        await self._send_data(write_value)

    async def play_midi(
        self,
        repetition: int = 0,
        operation: int = 3,
        midi_note_numbers: List[int, int, int] = [
            (30, 60, 255),
            (30, 62, 255),
            (30, 64, 255)
        ]
    ) -> None:
        """Plays the MIDI note number repeatedly.

        Args:
            repetition (int, optional): How many times to repeat the music.
                - Set it in [0, 255] and 0 is exceptionally infinite.
                - Defaults to 0.
            operation (int, optional): The number of operations.
                - Set it in [1, 59].
                - Defaults to 3.
            midi_note_numbers (List[int, int, int], optional): Playback time, MIDI note number, and volume of sound.
                - The element should be a tuple of (time, midi_note_number, volume).
                - time (int): Playback time (*10 ms) in [1, 255].
                - midi_note_number (int): MIDI note number in [0, 128].
                - volume (int): Volume of sound in [0, 255] and 0 for no sound.
                - Defaults to [(30, 60, 255), (30, 62, 255), (30, 64, 255)].
        """
        write_value = bytearray(b'\x03')
        write_value.append(repetition)
        write_value.append(operation)
        for playback_time, midi_note_num, volume in midi_note_numbers:
            write_value.append(playback_time)
            write_value.append(midi_note_num)
            write_value.append(volume)

        await self._send_data(write_value)
