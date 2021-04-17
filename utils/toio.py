from bleak import BleakClient
from characteristics import (Battery, Button, Configuration, Lamp,
                             MotionSensor, Motor, Reader, Sound)


class Toio:
    def __init__(
        self,
        name: str,
        address: str,
    ):
        self.__name = name
        self.__address = address
        self.__client = BleakClient(address_or_ble_device=address)
        self.__reader = Reader(name=self.__name, client=self.__client)
        self.__motor = Motor(name=self.__name, client=self.__client)
        self.__lamp = Lamp(name=self.__name, client=self.__client)
        self.__sound = Sound(name=self.__name, client=self.__client)
        self.__motion_sensor = MotionSensor(name=self.__name, client=self.__client)
        self.__button = Button(name=self.__name, client=self.__client)
        self.__battery = Battery(name=self.__name, client=self.__client)
        self.__configuration = Configuration(name=self.__name, client=self.__client)

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address

    @property
    def client(self):
        return self.__client

    @property
    def reader(self):
        return self.__reader

    @property
    def motor(self):
        return self.__motor

    @property
    def lamp(self):
        return self.__lamp

    @property
    def sound(self):
        return self.__sound

    @property
    def motion_sensor(self):
        return self.__motion_sensor

    @property
    def button(self):
        return self.__button

    @property
    def battery(self):
        return self.__battery

    @property
    def configuration(self):
        return self.__configuration
