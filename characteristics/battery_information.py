
from bleak import BleakClient
from utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Battery(AbstractCharacteristic):
    def __init__(self, name: str, client: BleakClient):
        super().__init__(
            uuid='10b20108-5b3b-4571-9508-cf3efcd7bbae',
            descriptor='Battery Information',
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client
        )

    def _notification_callback(self, _: int, data: bytearray):
        response = {
            'battery_remain': data[0]
        }
        logger.info(f'[{self.name}] [{self.descriptor}] {response}')

        return response
