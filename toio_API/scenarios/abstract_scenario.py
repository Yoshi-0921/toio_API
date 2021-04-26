# -*- coding: utf-8 -*-

import asyncio
from abc import ABC, abstractmethod
from typing import List

from toio_API.utils.general import connect, disconnect
from toio_API.utils.toio import Toio


class AbstractSenario(ABC):
    def __init__(self, toios: List[Toio]) -> None:
        self.__toios = toios

    @property
    def toios(self) -> List[Toio]:
        return self.__toios

    def run(self) -> None:
        asyncio.run(self.__run())

    async def __run(self) -> None:
        await self.__connect_toios()
        await self._main()
        await self.__disconnect_toios()

    async def __connect_toios(self) -> None:
        await asyncio.gather(*[connect(toio) for toio in self.__toios])

    async def __disconnect_toios(self) -> None:
        await asyncio.gather(*[disconnect(toio) for toio in self.__toios])

    @abstractmethod
    async def _main(self) -> None:
        raise NotImplementedError()
