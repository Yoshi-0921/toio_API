import asyncio
import math
import random
from utils.general import connect, disconnect
from utils.toio import Toio


MARGIN = 15


async def run(toio, **kwargs):
    try:
        # x:[98,402], y:[142,358]
        # x_minimum, y_minimum = 98 + MARGIN, 142 + MARGIN
        # width, height = 402 - MARGIN - x_minimum, 358 - MARGIN - y_minimum
        # x_coordinate = int(width * random.random()) + x_minimum
        # y_coordinate = int(height * random.random()) + y_minimum
        distance = math.dist(
            [kwargs['Yoshi']['center_x'], kwargs['Yoshi']['center_x']],
            [kwargs['Moto']['center_x'], kwargs['Moto']['center_x']]
        )
        print(distance)
        if distance < 120:
            await toio.motor.time_control(-10, -10, 5)
        else:
            # await toio.motor.target_control(time_out=5, movement=1, x_coordinate=x_coordinate, y_coordinate=y_coordinate)
            await toio.motor.control(50, 50)

    except Exception as e:
        print(e)


async def get_information(toio1, toio2):
    response1 = await toio1.reader.get_information()
    response2 = await toio2.reader.get_information()

    return {toio1.name: response1, toio2.name: response2}


async def main():
    toio1 = Toio(name='Yoshi', address='B62DBD30-1D16-4796-A60F-E76903A3BEF0')
    toio2 = Toio(name='Moto', address='33139358-E12D-45F8-9B83-A23EBC3CDD58')

    await asyncio.gather(connect(toio1), connect(toio2))

    for i in range(100):
        response = await get_information(toio1, toio2)
        await asyncio.gather(run(toio1, **response), run(toio2, **response))
        print(f'Task {i}: Done.')
        await asyncio.sleep(0.1)
    await asyncio.gather(disconnect(toio1), disconnect(toio2))


if __name__ == '__main__':
    asyncio.run(main())
