
import asyncio

from scenarios.abstract_scenario import AbstractSenario
from utils.general import start_notity


class Simple(AbstractSenario):
    async def _main(self):
        await asyncio.gather(*[start_notity(toio, battery=True) for toio in self.toios])

        for i in range(50):
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)
