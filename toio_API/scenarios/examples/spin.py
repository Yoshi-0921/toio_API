# -*- coding: utf-8 -*-

import asyncio

from toio_API.scenarios.abstract_scenario import AbstractSenario


class Spin(AbstractSenario):
    async def _main(self, **kwargs):
        while not kwargs['run'].is_set():
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)
