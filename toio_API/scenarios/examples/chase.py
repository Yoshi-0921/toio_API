# -*- coding: utf-8 -*-

import asyncio

from toio_API.scenarios.abstract_scenario import AbstractSenario
from toio_API.utils.general import read_information
from toio_API.utils.toio import Toio


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
            await toio.motor.target_control(
                max_speed=50,
                x_coordinate=kwargs[self.toios[toio_idx - 1].name]['center_x'],
                y_coordinate=kwargs[self.toios[toio_idx - 1].name]['center_y']
            )
