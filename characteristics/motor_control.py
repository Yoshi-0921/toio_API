
from characteristics.abstract_characteristic import AbstractCharacteristic


class Motor(AbstractCharacteristic):
    def __init__(self):
        super().__init__(
            uuid='10b20102-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Motor Control',
            write=False,
            write_without_response=True,
            read=True,
            notify=True
        )

