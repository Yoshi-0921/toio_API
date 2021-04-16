
from characteristics.abstract_characteristic import AbstractCharacteristic


class Button(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20107-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Button Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray):
        detection = {
            'button_state': data[1]
        }
        print(detection)
