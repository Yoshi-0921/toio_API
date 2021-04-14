
from utils.property import Property
from characteristics.abstract_characteristic import AbstractCharacteristic


class Battery(AbstractCharacteristic):
    _uuid = '10b20103-5b3b-4571-9508-cf3efcd7bbae'
    _descriptor = 'Light Control'
    _property = Property(write=True, write_without_response=False, read=False, notify=False)
