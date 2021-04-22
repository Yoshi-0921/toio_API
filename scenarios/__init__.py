# -*- coding: utf-8 -*-

from typing import List

from utils.logging import initialize_logging
from utils.toio import Toio

from .examples import BallChase, Chase, CollisionAvoidance, RunSpin, Spin

logger = initialize_logging(__name__)


def make_scenario(scenario_name: str = 'spin', toios: List[Toio] = None):
    if scenario_name == 'ball_chase':
        scenario = BallChase(toios=toios)

    elif scenario_name == 'chase':
        scenario = Chase(toios=toios)

    elif scenario_name == 'collision_avoidance':
        scenario = CollisionAvoidance(toios=toios)

    elif scenario_name == 'run_spin':
        scenario = RunSpin(toios=toios)

    elif scenario_name == 'spin':
        scenario = Spin(toios=toios)

    else:
        logger.warn(f'Invalid scenario name is given. scenario_name: {scenario_name}')

        raise ValueError()

    return scenario
