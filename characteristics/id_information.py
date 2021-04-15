
from characteristics.abstract_characteristic import AbstractCharacteristic


class Reader(AbstractCharacteristic):
    def __init__(self):
        super().__init__(
            uuid='10b20101-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='ID Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True
        )
