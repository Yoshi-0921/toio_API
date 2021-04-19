
from bleak import BleakClient
from utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Battery(AbstractCharacteristic):
    """Battery characteristic.
    """
    def __init__(self, name: str = None, client: BleakClient = None):
        """Initialize the battery characteristic used in Toio.

        Args:
            name (str, optional): Name of toio. Defaults to None.
            client (BleakClient, optional): BleakClient to connect via BLE connection. Defaults to None.
        """
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
