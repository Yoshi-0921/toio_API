# -*- coding: utf-8 -*-

import asyncio

from scenarios.abstract_scenario import AbstractSenario


class Simple(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)
