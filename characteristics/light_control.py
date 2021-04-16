
from characteristics.abstract_characteristic import AbstractCharacteristic


class Lamp(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b20103-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Light Control',
            write=True,
            write_without_response=False,
            read=False,
            notify=False,
            client=client
        )

