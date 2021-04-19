from bleak import BleakClient
from characteristics import (Battery, Button, Configuration, Lamp,
                             MagneticSensor, MotionSensor, Motor, Reader,
                             Sound)


class Toio:
    """Toio to control.
    """
    def __init__(
        self,
        name: str = None,
        address: str = None,
    ) -> None:
        """Initialize toio to start controlling.

        Args:
            name (str, optional): Name of toio. Defaults to None.
            address (str, optional): Bluetooth device address of toio in small letter. Defaults to None.
        """
        self.__name = name
        self.__address = address
        self.__client = BleakClient(address_or_ble_device=address)
        self.__reader = Reader(name=self.__name, client=self.__client)
        self.__motor = Motor(name=self.__name, client=self.__client)
        self.__lamp = Lamp(name=self.__name, client=self.__client)
        self.__sound = Sound(name=self.__name, client=self.__client)
        self.__motion_sensor = MotionSensor(name=self.__name, client=self.__client)
        self.__magnetic_sensor = MagneticSensor(name=self.__name, client=self.__client)
        self.__button = Button(name=self.__name, client=self.__client)
        self.__battery = Battery(name=self.__name, client=self.__client)
        self.__configuration = Configuration(name=self.__name, client=self.__client)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def address(self) -> str:
        return self.__address

    @property
    def client(self) -> BleakClient:
        return self.__client

    @property
    def reader(self) -> Reader:
        return self.__reader

    @property
    def motor(self) -> Motor:
        return self.__motor

    @property
    def lamp(self) -> Lamp:
        return self.__lamp

    @property
    def sound(self) -> Sound:
        return self.__sound

    @property
    def motion_sensor(self) -> MotionSensor:
        return self.__motion_sensor

    @property
    def magnetic_sensor(self) -> MagneticSensor:
        return self.__magnetic_sensor

    @property
    def button(self) -> Button:
        return self.__button

    @property
    def battery(self) -> Battery:
        return self.__battery

    @property
    def configuration(self) -> Configuration:
        return self.__configuration
