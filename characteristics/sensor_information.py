
from utils.property import Property
from characteristics.abstract_characteristic import AbstractCharacteristic


class Sensor(AbstractCharacteristic):
    _uuid = '10b20106-5b3b-4571-9508-cf3efcd7bbae'
    _descriptor = 'Sensor Information'
    _property = Property(write=True, write_without_response=False, read=True, notify=True)
