from typing import List

from toio_API.utils.logging import initialize_logging
from toio_API.utils.toio import Toio

from .examples import (AimDests, BallChase, Chase, CollisionAvoidance,
                       JoyControl, RunSpin, Spin)

logger = initialize_logging(__name__)


SCENARIOS = [
    "aim_dests",
    "ball_chanse",
    "chase",
    "collision_avoidance",
    "run_spin",
    "spin",
    "control",
]


def make_scenario(scenario_name: str = "spin", toios: List[Toio] = None):
    if scenario_name == "aim_dests":
        scenario = AimDests(toios=toios)

    elif scenario_name == "ball_chase":
        scenario = BallChase(toios=toios)

    elif scenario_name == "chase":
        scenario = Chase(toios=toios)

    elif scenario_name == "collision_avoidance":
        scenario = CollisionAvoidance(toios=toios)

    elif scenario_name == "run_spin":
        scenario = RunSpin(toios=toios)

    elif scenario_name == "spin":
        scenario = Spin(toios=toios)

    elif scenario_name == "control":
        scenario = JoyControl(toios=toios)

    else:
        logger.warn(f"Invalid scenario name is given. scenario_name: {scenario_name}")

        raise ValueError()

    return scenario
