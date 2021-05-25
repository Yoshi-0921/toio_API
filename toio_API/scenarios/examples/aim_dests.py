# -*- coding: utf-8 -*-

import asyncio
import math
from toio_API.scenarios.abstract_scenario import AbstractSenario
from toio_API.utils.general import read_information
from toio_API.utils.toio import Toio


class AimDests(AbstractSenario):
    async def _main(self):
        self.dests = [[(350, 300), (350, 170), (120, 170), (140, 300)] for _ in range(self.num_toios)]
        for _ in range(100):
            response = await read_information(self.toios)
            await asyncio.gather(*[self.__aim(toio, toio_idx, **response) for toio_idx, toio in enumerate(self.toios)])
            await asyncio.sleep(0.1)

    async def __aim(self, toio: Toio, toio_idx: int, **kwargs):
        if self.dests[toio_idx]:
            x_coordinate = kwargs[self.toios[toio_idx].name]['center_x']
            y_coordinate = kwargs[self.toios[toio_idx].name]['center_y']

            if math.dist(self.dests[toio_idx][0], (x_coordinate, y_coordinate)) < 10:
                self.dests[toio_idx].pop(0)

        if self.dests[toio_idx]:
            aiming_dest_x, aiming_dest_y = self.dests[toio_idx][0]

            await toio.motor.target_control(
                max_speed=50,
                x_coordinate=aiming_dest_x,
                y_coordinate=aiming_dest_y
            )

        else:
            await toio.motor.control(left_speed=0, right_speed=0)
