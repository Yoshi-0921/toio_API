
from bleak import BleakClient

from characteristics.abstract_characteristic import AbstractCharacteristic


class Configuration(AbstractCharacteristic):
    def __init__(self, name: str, client: BleakClient):
        super().__init__(
            uuid='10b201ff-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Configuration',
            write=True,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )
