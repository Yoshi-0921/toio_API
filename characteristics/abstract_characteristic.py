
from abc import ABC


class AbstractCharacteristic(ABC):
    @classmethod
    def get_uuid(self):
        return self._uuid

    @classmethod
    def get_descriptor(self):
        return self._descriptor

    @classmethod
    def get_property(self):
        return self._property
