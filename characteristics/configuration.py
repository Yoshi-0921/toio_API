
from characteristics.abstract_characteristic import AbstractCharacteristic


class Configuration(AbstractCharacteristic):
    def __init__(self, client):
        super().__init__(
            uuid='10b201ff-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Configuration',
            write=True,
            write_without_response=False,
            read=True,
            notify=True,
            client=client
        )
