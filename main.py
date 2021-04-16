import asyncio
import random
from utils.toio import Toio


async def run(toio):
    try:
        await toio.client.connect()
        await toio.motion_sensor.start_notify()
        await toio.battery.start_notify()
        while 1:
            x_coordinate = int(300 * random.random()) + 98
            y_coordinate = int(200 * random.random()) + 150
            await toio.motor.target_control(time_out=5, x_coordinate=x_coordinate, y_coordinate=y_coordinate)
            await asyncio.sleep(5.0)
            # await toio.motion_sensor.get_information()
            # x:[98,402], y:[142,358]
    except Exception as e:
        print(e)
    finally:
        await toio.client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    toio1 = Toio(name='Yoshi', address='B62DBD30-1D16-4796-A60F-E76903A3BEF0')
    toio2 = Toio(name='Moto', address='33139358-E12D-45F8-9B83-A23EBC3CDD58')

    gather = asyncio.gather(
        run(toio1),
        run(toio2)
    )

    loop.run_until_complete(gather)
