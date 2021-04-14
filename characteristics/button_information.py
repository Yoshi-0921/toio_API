
from utils.property import Property
from characteristics.abstract_characteristic import AbstractCharacteristic


class Button(AbstractCharacteristic):
    _uuid = '10b20107-5b3b-4571-9508-cf3efcd7bbae'
    _descriptor = 'Button Information'
    _property = Property(write=False, write_without_response=False, read=True, notify=True)
