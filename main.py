import asyncio
import random
from utils.toio import Toio


MARGIN = 15


async def run(toio):
    try:
        await toio.client.connect()
        await toio.motion_sensor.start_notify()
        await toio.battery.start_notify()
        await toio.button.start_notify()
        await toio.lamp.consecutive_switch()
        x_minimum, y_minimum = 98 + MARGIN, 142 + MARGIN
        width, height = 402 - MARGIN - x_minimum, 358 - MARGIN - y_minimum
        while 1:
            x_coordinate = int(width * random.random()) + x_minimum
            y_coordinate = int(height * random.random()) + y_minimum
            await toio.motor.target_control(time_out=5, movement=1, x_coordinate=x_coordinate, y_coordinate=y_coordinate)
            await asyncio.sleep(5.0)
            await toio.reader.get_information()
            # x:[98,402], y:[142,358]
    except Exception as e:
        print(e)
    finally:
        await toio.client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    toio1 = Toio(name='Yoshi', address='B62DBD30-1D16-4796-A60F-E76903A3BEF0')
    # toio2 = Toio(name='Moto', address='33139358-E12D-45F8-9B83-A23EBC3CDD58')

    gather = asyncio.gather(
        run(toio1),
        # run(toio2)
    )

    loop.run_until_complete(gather)
