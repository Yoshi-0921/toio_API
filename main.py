"""Source code for the main entry.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

import asyncio

from toio_API.scenarios import make_scenario
from toio_API.utils.general import create_toios, discover_toios

if __name__ == "__main__":
    toio_addresses = asyncio.run(discover_toios())
    toios = create_toios(
        toio_addresses=toio_addresses
    )
    scenario = make_scenario(scenario_name="joy_stick", toios=toios)

    scenario.run()
