# -*- coding: utf-8 -*-

from scenarios import make_scenario
from utils.toio import Toio

if __name__ == '__main__':
    toio1 = Toio(name='Yoshi', address='B62DBD30-1D16-4796-A60F-E76903A3BEF0')
    toio2 = Toio(name='Moto', address='33139358-E12D-45F8-9B83-A23EBC3CDD58')
    scenario = make_scenario(scenario_name='collision_avoidance', toios=[toio1, toio2])

    scenario.run()
