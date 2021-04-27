# -*- coding: utf-8 -*-

import asyncio

from toio_API.scenarios import make_scenario
from toio_API.utils.general import create_toios, discover_toios

if __name__ == '__main__':
    toio_addresses = asyncio.run(discover_toios())
    toios = create_toios(toio_addresses=toio_addresses, toio_names=['Yoshi', 'Moto'])
    scenario = make_scenario(scenario_name='ball_chase', toios=toios)

    scenario.run()
