# -*- coding: utf-8 -*-

import asyncio
from utils.toio import Toio
from scenarios.abstract_scenario import AbstractSenario
from utils.general import read_information
import math


class Chase(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            response = await read_information(self.toios)
            await asyncio.gather(*[self.__chase(toio, toio_idx, **response) for toio_idx, toio in enumerate(self.toios)])
            await asyncio.sleep(0.1)

    async def __chase(self, toio: Toio, toio_idx: int, **kwargs):
        if toio_idx == 0:
            await toio.motor.acceleration_control(rotation_speed=90)
        else:
            distance = math.dist(
                [kwargs[self.toios[0].name]['center_x'], kwargs[self.toios[0].name]['center_y']],
                [kwargs[toio.name]['center_x'], kwargs[toio.name]['center_y']]
            )
            if distance < 50:
                await toio.motor.control(left_speed=0, right_speed=0)
            else:
                await toio.motor.target_control(
                    max_speed=50,
                    x_coordinate=kwargs[self.toios[0].name]['center_x'],
                    y_coordinate=kwargs[self.toios[0].name]['center_y']
                )
