# -*- coding: utf-8 -*-

import asyncio
import math

from scenarios.abstract_scenario import AbstractSenario
from utils.general import read_information
from utils.toio import Toio


class CollisionAvoidance(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            response = await read_information(self.toios)
            await asyncio.gather(*[self.__chase(toio, toio_idx, **response) for toio_idx, toio in enumerate(self.toios)])
            await asyncio.sleep(0.01)

    async def __chase(self, toio: Toio, toio_idx: int, **kwargs):
        distance = math.dist(
            [kwargs[self.toios[0].name]['center_x'], kwargs[self.toios[0].name]['center_y']],
            [kwargs[self.toios[1].name]['center_x'], kwargs[self.toios[1].name]['center_y']]
        )
        if distance < 70:
            await toio.motor.control(-10, -10)
        else:
            await toio.motor.control(left_speed=50, right_speed=50)
