# -*- coding: utf-8 -*-

import asyncio
from utils.toio import Toio
from scenarios.abstract_scenario import AbstractSenario


class RunSpin(AbstractSenario):
    async def _main(self):
        await asyncio.gather(*[self.__run_spin(toio) for toio in self.toios])

    async def __run_spin(self, toio: Toio):
        await toio.motor.control(left_speed=100, right_speed=100)
        await asyncio.sleep(1)
        await toio.motor.control(left_speed=-100, right_speed=100)
        await asyncio.sleep(1)
