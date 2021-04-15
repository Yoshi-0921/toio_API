
from characteristics.abstract_characteristic import AbstractCharacteristic


class MotionSensor(AbstractCharacteristic):
    def __init__(self):
        super().__init__(
            uuid='10b20106-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Sensor Information',
            write=True,
            write_without_response=False,
            read=True,
            notify=True
        )

