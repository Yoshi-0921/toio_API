# -*- coding: utf-8 -*-

import asyncio
import cv2
from toio_API.camera.ball import convert_ball_position, get_ball_center
from toio_API.scenarios.abstract_scenario import AbstractSenario
from toio_API.utils.general import read_information
from toio_API.utils.toio import Toio
import math


class BallChase(AbstractSenario):
    async def _main(self, **kwargs):
        capture = cv2.VideoCapture(1)

        while not kwargs['run'].is_set():
            response = await read_information(self.toios)
            response = get_ball_center(capture, **response)
            response = convert_ball_position(
                board_x1=98, board_y1=142, board_x2=402, board_y2=358,
                camera_x1=370, camera_y1=110, camera_x2=1720, camera_y2=1000, **response
            )
            await asyncio.gather(*[self.__chase(toio, toio_idx, **response) for toio_idx, toio in enumerate(self.toios)])
            await asyncio.sleep(0.1)

    async def __chase(self, toio: Toio, toio_idx: int, **kwargs):
        if toio_idx == 0:
            try:
                ball_x, ball_y = kwargs['ball_center']
                await toio.motor.target_control(x_coordinate=ball_x, y_coordinate=ball_y)
            except TypeError:
                await toio.motor.target_control(x_coordinate=250, y_coordinate=250)
        else:
            distance = math.dist(
                [kwargs[self.toios[0].name]['center_x'], kwargs[self.toios[0].name]['center_y']],
                [kwargs[self.toios[1].name]['center_x'], kwargs[self.toios[1].name]['center_y']]
            )
            if distance < 75:
                await toio.motor.control(left_speed=0, right_speed=0)

            elif distance < 50:
                await toio.motor.control(left_speed=-10, right_speed=-10)

            else:
                await toio.motor.target_control(
                    max_speed=50,
                    x_coordinate=kwargs[self.toios[0].name]['center_x'],
                    y_coordinate=kwargs[self.toios[0].name]['center_y']
                )
