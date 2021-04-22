# -*- coding: utf-8 -*-

from scenarios.abstract_scenario import AbstractSenario


class Custom3(AbstractSenario):
    async def _main(self):
        raise NotImplementedError()
