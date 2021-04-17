
from .abstract_characteristic import AbstractCharacteristic


class Reader(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20101-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='ID Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray):
        if len(data) == 1:
            print('Position ID missed')
        else:
            detection = {
                'center_x': int.from_bytes(data[1:3], 'little'),
                'center_y': int.from_bytes(data[3:5], 'little'),
                'center_theta': int.from_bytes(data[5:7], 'little'),
                'sensor_x': int.from_bytes(data[7:9], 'little'),
                'sensor_y': int.from_bytes(data[9:11], 'little'),
                'sensor_theta': int.from_bytes(data[11:13], 'little')
            }

            return detection
