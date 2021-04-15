import asyncio
from utils.toio import Toio


async def run(toio):
    try:
        await toio.client.connect()
        # await toio.motor.control()
        # await toio.motor.time_control(time=10)
        await toio.motor.targets_control()
        await asyncio.sleep(5.0)
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
