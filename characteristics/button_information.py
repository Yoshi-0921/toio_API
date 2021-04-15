
from characteristics.abstract_characteristic import AbstractCharacteristic


class Button(AbstractCharacteristic):
    def __init__(self):
        super().__init__(
            uuid='10b20107-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Button Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True
        )
