
from .abstract_characteristic import AbstractCharacteristic


class Battery(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20108-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Battery Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray):
        detection = {
            'battery_remain': data[0]
        }
        print(detection)
