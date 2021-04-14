
from utils.property import Property
from characteristics.abstract_characteristic import AbstractCharacteristic


class Motor(AbstractCharacteristic):
    _uuid = '10b20102-5b3b-4571-9508-cf3efcd7bbae'
    _descriptor = 'Motor Control'
    _property = Property(write=False, write_without_response=True, read=True, notify=True)
