
from utils.property import Property


class Configuration:
    __uuid = '10b201ff-5b3b-4571-9508-cf3efcd7bbae'
    __descriptor = 'Configuration'
    __property = Property(write=True, write_without_response=False, read=True, notify=True)

    @classmethod
    def get_uuid(self):
        return self.__uuid

    @classmethod
    def get_descriptor(self):
        return self.__descriptor

    @classmethod
    def get_property(self):
        return self.__property
