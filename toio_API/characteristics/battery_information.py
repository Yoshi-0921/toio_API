"""Source code for the Battery characteristic class.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

from typing import Dict

from bleak import BleakClient
from toio_API.utils.logging import initialize_logging

from .abstract_characteristic import AbstractCharacteristic

logger = initialize_logging(__name__)


class Battery(AbstractCharacteristic):
    """Battery characteristic.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_battery.

    Args:
        name (str, optional): Name of toio.
            - Defaults to None.
        client (BleakClient, optional): BleakClient to connect via BLE connection.
            - Defaults to None.
    """

    def __init__(self, name: str = None, client: BleakClient = None) -> None:
        super().__init__(
            uuid="10b20108-5b3b-4571-9508-cf3efcd7bbae",
            descriptor="Battery Information",
            write=False,
            write_without_response=False,
            read=True,
            notify=True,
            name=name,
            client=client,
        )

    def _notification_callback(self, _: int, data: bytearray) -> Dict[str, int]:
        """Decode binary information from the battry characteristic.

        Args:
            _ (int): Not used in this method.
            data (bytearray): Binary data from the battery characteristic.

        Returns:
            Dict[str, int]: Decoded information.
        """
        response = {"battery_remain": data[0]}
        logger.info(f"[{self.name}] [{self.descriptor}] {response}")

        return response
