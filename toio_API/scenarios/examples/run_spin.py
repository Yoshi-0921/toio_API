"""Source code for the RunSpin scenario class.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

import asyncio

from toio_API.scenarios.abstract_scenario import AbstractScenario
from toio_API.utils.toio import Toio


class RunSpin(AbstractScenario):
    async def _main(self, **kwargs):
        await asyncio.gather(*[self.__run_spin(toio) for toio in self.toios])

    async def __run_spin(self, toio: Toio):
        await toio.motor.control(left_speed=100, right_speed=100)
        await asyncio.sleep(1)
        await toio.motor.control(left_speed=-100, right_speed=100)
        await asyncio.sleep(1)
