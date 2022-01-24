"""Source code for the CollisionAvoidance scenario class.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

import asyncio
import math

from toio_API.scenarios.abstract_scenario import AbstractScenario
from toio_API.utils.general import read_information
from toio_API.utils.toio import Toio


class CollisionAvoidance(AbstractScenario):
    async def _main(self, **kwargs):
        while not kwargs["run"].is_set():
            response = await read_information(self.toios)
            await asyncio.gather(
                *[
                    self.__chase(toio, toio_idx, **response)
                    for toio_idx, toio in enumerate(self.toios)
                ]
            )
            await asyncio.sleep(0.01)

    async def __chase(self, toio: Toio, toio_idx: int, **kwargs):
        distance = math.dist(
            [
                kwargs[self.toios[0].name]["center_x"],
                kwargs[self.toios[0].name]["center_y"],
            ],
            [
                kwargs[self.toios[1].name]["center_x"],
                kwargs[self.toios[1].name]["center_y"],
            ],
        )
        if distance < 70:
            await toio.motor.control(-10, -10)
        else:
            await toio.motor.control(left_speed=50, right_speed=50)
