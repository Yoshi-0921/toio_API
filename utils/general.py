
from bleak import BleakError

from utils.logging import initialize_logging
from utils.toio import Toio

logger = initialize_logging(__name__)


async def connect(toio: Toio):
    """Connects toio to the computer using BLE connection.

    Args:
        toio (Toio): Toio to connect.
    """
    try:
        await toio.client.connect()
        logger.info(f'[{toio.name}] Toio connected!')

    except BleakError:
        logger.exception(f'[{toio.name}] Failed to connect.')


async def disconnect(toio: Toio):
    """Disconnects toio from the computer.

    Args:
        toio (Toio): Toio to disconnect.
    """
    try:
        await toio.client.disconnect()
        logger.info(f'[{toio.name}] Toio disonnected!')

    except BleakError:
        logger.exception(f'[{toio.name}] Failed to disconnect.')


async def start_notity(
    toio: Toio,
    reader: bool = False,
    motor: bool = False,
    motion_sensor: bool = False,
    magnetic_sensor: bool = False,
    button: bool = False,
    battery: bool = False
):
    """Starts notification of specific toio characteristics.

    Args:
        toio (Toio): Toio to set.
        reader (bool, optional): ID information. Defaults to False.
        motor (bool, optional): Motor control. Defaults to False.
        motion_sensor (bool, optional): Sensor information. Defaults to False.
        magnetic_sensor (bool, optional): Magnetic sensor information. Defaults to False.
        button (bool, optional): Button information. Defaults to False.
        battery (bool, optional): Battery information. Defaults to False.
    """
    try:
        if reader:
            await toio.reader.start_notify()
            logger.info(f'[{toio.name}] Start reader notification!')

        if motor:
            await toio.motor.start_notify()
            logger.info(f'[{toio.name}] Start motor notification!')

        if motion_sensor:
            await toio.motion_sensor.start_notify()
            logger.info(f'[{toio.name}] Start motion sensor notification!')

        if magnetic_sensor:
            await toio.magnetic_sensor.start_notify()
            logger.info(f'[{toio.name}] Start magnetic sensor notification!')

        if button:
            await toio.reader.start_notify()
            logger.info(f'[{toio.name}] Start button notification!')

        if battery:
            await toio.reader.start_notify()
            logger.info(f'[{toio.name}] Start battery notification!')

    except BleakError:
        logger.exception(f'[{toio.name}] Failed to start notification.')


async def stop_notity(
    toio: Toio,
    reader: bool = False,
    motor: bool = False,
    motion_sensor: bool = False,
    magnetic_sensor: bool = False,
    button: bool = False,
    battery: bool = False
):
    """Stops notification of specific toio characteristics.

    Args:
        toio (Toio): Toio to set.
        reader (bool, optional): ID information. Defaults to False.
        motor (bool, optional): Motor control. Defaults to False.
        motion_sensor (bool, optional): Sensor information. Defaults to False.
        magnetic_sensor (bool, optional): Magnetic sensor information. Defaults to False.
        button (bool, optional): Button information. Defaults to False.
        battery (bool, optional): Battery information. Defaults to False.
    """
    try:
        if reader:
            await toio.reader.stop_notify()
            logger.info(f'[{toio.name}] Stop reader notification!')

        if motor:
            await toio.motor.stop_notify()
            logger.info(f'[{toio.name}] Stop motor notification!')

        if motion_sensor:
            await toio.motion_sensor.stop_notify()
            logger.info(f'[{toio.name}] Stop motion sensor notification!')

        if magnetic_sensor:
            await toio.magnetic_sensor.stop_notify()
            logger.info(f'[{toio.name}] Stop magnetic sensor notification!')

        if button:
            await toio.reader.stop_notify()
            logger.info(f'[{toio.name}] Stop button notification!')

        if battery:
            await toio.reader.stop_notify()
            logger.info(f'[{toio.name}] Stop battery notification!')

    except BleakError:
        logger.exception(f'[{toio.name}] Failed to stop notification.')
