# -*- coding: utf-8 -*-

import asyncio
import math
import cv2
import random
from utils.general import connect, start_notity, disconnect
from utils.toio import Toio
from camera.ball import get_ball_center, convert_ball_position

MARGIN = 50


async def run(toio, **kwargs):
    try:
        # x:[98,402], y:[142,358]
        x_minimum, y_minimum = 98 + MARGIN, 142 + MARGIN
        x_maximum, y_maximum = 402 - MARGIN, 358 - MARGIN
        width, height = 402 - MARGIN - x_minimum, 358 - MARGIN - y_minimum
        x_coordinate = int(width * random.random()) + x_minimum
        y_coordinate = int(height * random.random()) + y_minimum

        if toio.name == 'Yoshi':
            # await toio.motor.acceleration_control(rotation_speed=90)
            await toio.motor.target_control(x_coordinate=250, y_coordinate=300, theta_type=5)
            # if kwargs['ball_center'] is None:
            #    await toio.motor.target_control(x_coordinate=223, y_coordinate=267)
            # await toio.motor.target_control(x_coordinate=kwargs['ball_center'][0], y_coordinate=kwargs['ball_center'][1])
        else:
            try:
                distance = math.dist(
                    [kwargs['Yoshi']['center_x'], kwargs['Yoshi']['center_y']],
                    [kwargs['Moto']['center_x'], kwargs['Moto']['center_y']]
                )
                if distance < 50:
                    await toio.motor.control(left_speed=0, right_speed=0)
                else:
                    await toio.motor.target_control(
                        max_speed=50,
                        x_coordinate=kwargs['Yoshi']['center_x'],
                        y_coordinate=kwargs['Yoshi']['center_y']
                    )
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


async def read_information(toio1, toio2):
    response1 = await toio1.reader.read_information()
    response2 = await toio2.reader.read_information()

    return {toio1.name: response1, toio2.name: response2}


async def main():
    toio1 = Toio(name='Yoshi', address='B62DBD30-1D16-4796-A60F-E76903A3BEF0')
    toio2 = Toio(name='Moto', address='33139358-E12D-45F8-9B83-A23EBC3CDD58')
    cap = cv2.VideoCapture(1)

    await asyncio.gather(connect(toio1))#, connect(toio2))

    await asyncio.gather(start_notity(toio1, motion_sensor=True, battery=True), start_notity(toio2, motion_sensor=True, battery=True))

    while 1:
        response = await read_information(toio1, toio2)
        # response = get_ball_center(cap, **response)
        # response = convert_ball_position(98, 142, 402, 358, 240, 100, 1260, 800, **response)
        await asyncio.gather(run(toio1, **response), run(toio2, **response))
        await asyncio.sleep(0.1)

    await asyncio.gather(disconnect(toio1), disconnect(toio2))


if __name__ == '__main__':
    asyncio.run(main())
