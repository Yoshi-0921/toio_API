"""Source code for the utility methods.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

from typing import Dict, List

from bleak import BleakError, discover

from toio_API.utils.logging import initialize_logging
from toio_API.utils.toio import Toio

logger = initialize_logging(__name__)


def create_toios(
    toio_addresses: List[str] = None, toio_names: List[str] = None
) -> List[Toio]:
    """Creates toios based on given adresses and names.

    Args:
        toio_addresses (List[str], optional): Bleak client address of toio from discover_toios method.
            - Defaults to None.
        toio_names (List[str], optional): Names of toio.
            - Set it None for default names: ['toio_0', 'toio_1', ...]
            - Defaults to None.

    Returns:
        List[Toio]: Registered set of toio.
    """
    toio_names = toio_names or [
        f"toio_{toio_idx}" for toio_idx in range(len(toio_addresses))
    ]
    toios = [
        Toio(address=toio_address, name=toio_name)
        for toio_address, toio_name in zip(toio_addresses, toio_names)
    ]

    if len(toios):
        logger.info(
            f"{len(toios)} Successfully registered the toio: {toio_names[:len(toios)]}"
        )
    else:
        logger.info("No toio registred :(")

    return toios


async def discover_toios() -> List[str]:
    """Discover toio within BLE connection range.

    Returns:
        List[str]: Bleak client addresses of toio.
    """
    devices = await discover()
    toio_addresses = [d.address for d in devices if "toio Core" in d.name]

    if len(toio_addresses):
        logger.info(f"{len(toio_addresses)} toio discovered: {toio_addresses}")
    else:
        logger.info("No toio discovered :(")

    return toio_addresses


async def connect(toio: Toio) -> None:
    """Connects the toio to the computer using BLE connection.

    Args:
        toio (Toio): Your toio to connect.
    """
    try:
        await toio.client.connect()
        logger.info(f"[{toio.name}] Successfully connected the toio!")

    except BleakError:
        logger.exception(f"[{toio.name}] Failed to connect the toio: {toio.address}.")

    except TimeoutError:
        logger.exception(f"[{toio.name}] Timeout to connect the toio: {toio.address}.")


async def disconnect(toio: Toio) -> None:
    """Disconnects the toio from the computer.

    Args:
        toio (Toio): Your toio to disconnect.
    """
    try:
        await toio.client.disconnect()
        logger.info(f"[{toio.name}] Successfully disonnected the toio!")

    except BleakError:
        logger.exception(
            f"[{toio.name}] Failed to disconnect the toio: {toio.address}."
        )

    except TimeoutError:
        logger.exception(
            f"[{toio.name}] Timeout to disconnect the toio: {toio.address}."
        )


async def start_notity(
    toio: Toio,
    reader: bool = False,
    motor: bool = False,
    motion_sensor: bool = False,
    magnetic_sensor: bool = False,
    button: bool = False,
    battery: bool = False,
) -> None:
    """Starts notification of specific toio characteristics.

    Args:
        toio (Toio): Your toio to set.
        reader (bool, optional): ID information.
            - Defaults to False.
        motor (bool, optional): Motor control.
            - Defaults to False.
        motion_sensor (bool, optional): Sensor information.
            - Defaults to False.
        magnetic_sensor (bool, optional): Magnetic sensor information.
            - Defaults to False.
        button (bool, optional): Button information.
            - Defaults to False.
        battery (bool, optional): Battery information.
            - Defaults to False.
    """
    try:
        if reader:
            await toio.reader.start_notify()
            logger.info(f"[{toio.name}] Start reader notification!")

        if motor:
            await toio.motor.start_notify()
            logger.info(f"[{toio.name}] Start motor notification!")

        if motion_sensor:
            await toio.motion_sensor.start_notify()
            logger.info(f"[{toio.name}] Start motion sensor notification!")

        if magnetic_sensor:
            await toio.magnetic_sensor.start_notify()
            logger.info(f"[{toio.name}] Start magnetic sensor notification!")

        if button:
            await toio.reader.start_notify()
            logger.info(f"[{toio.name}] Start button notification!")

        if battery:
            await toio.reader.start_notify()
            logger.info(f"[{toio.name}] Start battery notification!")

    except BleakError:
        logger.exception(f"[{toio.name}] Failed to start notification.")


async def stop_notity(
    toio: Toio,
    reader: bool = False,
    motor: bool = False,
    motion_sensor: bool = False,
    magnetic_sensor: bool = False,
    button: bool = False,
    battery: bool = False,
) -> None:
    """Stops notification of specific toio characteristics.

    Args:
        toio (Toio): Your toio to set.
        reader (bool, optional): ID information.
            - Defaults to False.
        motor (bool, optional): Motor control.
            - Defaults to False.
        motion_sensor (bool, optional): Sensor information.
            - Defaults to False.
        magnetic_sensor (bool, optional): Magnetic sensor information.
            - Defaults to False.
        button (bool, optional): Button information.
            - Defaults to False.
        battery (bool, optional): Battery information.
            - Defaults to False.
    """
    try:
        if reader:
            await toio.reader.stop_notify()
            logger.info(f"[{toio.name}] Stop reader notification!")

        if motor:
            await toio.motor.stop_notify()
            logger.info(f"[{toio.name}] Stop motor notification!")

        if motion_sensor:
            await toio.motion_sensor.stop_notify()
            logger.info(f"[{toio.name}] Stop motion sensor notification!")

        if magnetic_sensor:
            await toio.magnetic_sensor.stop_notify()
            logger.info(f"[{toio.name}] Stop magnetic sensor notification!")

        if button:
            await toio.reader.stop_notify()
            logger.info(f"[{toio.name}] Stop button notification!")

        if battery:
            await toio.reader.stop_notify()
            logger.info(f"[{toio.name}] Stop battery notification!")

    except BleakError:
        logger.exception(f"[{toio.name}] Failed to stop notification.")


async def read_information(toios: List[Toio]) -> Dict[str, str]:
    """Reads ID information from the toios.

    Args:
        toios (List[Toio]): Set of toios to get information.

    Returns:
        Dict[str, str]: Decoded information.
    """
    resposes = {}
    for toio in toios:
        resposes[toio.name] = await toio.reader.read_information()

    return resposes
