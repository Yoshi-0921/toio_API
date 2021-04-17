from utils.toio import Toio
from utils.logging import initialize_logging
logger = initialize_logging(__name__)


async def connect(toio: Toio):
    await toio.client.connect()

    logger.info(f'[{toio.name}] Connected!')


async def start_notity(
    toio: Toio,
    reader: bool = False,
    motor: bool = False,
    motion_sensor: bool = False,
    magnetic_sensor: bool = False,
    button: bool = False,
    battery: bool = False
):
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


async def disconnect(toio: Toio):
    await toio.client.disconnect()
    logger.info(f'[{toio.name}] Disonnected!')
