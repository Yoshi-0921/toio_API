async def connect(toio):
    await toio.client.connect()
    # await toio.motion_sensor.start_notify()
    await toio.battery.start_notify()
    await toio.button.start_notify()
    await toio.lamp.consecutive_switch()
    print(f'[{toio.name}] Connected!')


async def disconnect(toio):
    await toio.client.disconnect()
    print(f'[{toio.name}] Disonnected!')
