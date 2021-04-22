# -*- coding: utf-8 -*-

from scenarios.abstract_scenario import AbstractSenario


class Custom1(AbstractSenario):
    async def _main(self):
        raise NotImplementedError()
