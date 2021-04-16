
from .abstract_characteristic import AbstractCharacteristic


class MotionSensor(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20106-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Sensor Information',
            write=True,
            write_without_response=False,
            read=True,
            notify=True,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray):
        detection = {
            'level': data[1],
            'collision': data[2],
            'double_tap': data[3],
            'posture': data[4],
            'shake': data[5]
        }
        print(detection)
