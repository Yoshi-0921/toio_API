"""Source code for the Spin scenario class.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

import asyncio

from toio_API.scenarios.abstract_scenario import AbstractScenario


class Spin(AbstractScenario):
    async def _main(self, **kwargs):
        while not kwargs["run"].is_set():
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)
