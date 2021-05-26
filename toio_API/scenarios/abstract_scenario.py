# -*- coding: utf-8 -*-

import asyncio
from abc import ABC, abstractmethod
from typing import List

from toio_API.utils.general import connect, disconnect
from toio_API.utils.toio import Toio


class AbstractSenario(ABC):
    def __init__(self, toios: List[Toio]) -> None:
        self.__toios = toios
        self.__num_toios = len(self.__toios)

    @property
    def toios(self) -> List[Toio]:
        return self.__toios

    @property
    def num_toios(self) -> int:
        return self.__num_toios

    def run(self, **kwargs) -> None:
        asyncio.run(self.__run(**kwargs))

    async def __run(self, **kwargs) -> None:
        await self.__connect_toios()
        await self._main(**kwargs)
        await self.__disconnect_toios()

    async def __connect_toios(self) -> None:
        await asyncio.gather(*[connect(toio) for toio in self.__toios])

    async def __disconnect_toios(self) -> None:
        await asyncio.gather(*[disconnect(toio) for toio in self.__toios])

    @abstractmethod
    async def _main(self, **kwargs) -> None:
        raise NotImplementedError()
