
from .examples.simple import Simple
from typing import List
from utils.toio import Toio
from utils.logging import initialize_logging
logger = initialize_logging(__name__)


def make_scenario(scenario_name: str = 'simple', toios: List[Toio] = None):
    if scenario_name == 'simple':
        scenario = Simple(toios)

    else:
        logger.warn(f'Invalid scenario name is given. scenario_name: {scenario_name}')

        raise ValueError()

    return scenario
