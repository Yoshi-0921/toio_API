# -*- coding: utf-8 -*-

from bleak import BleakClient
from toio_API.characteristics import (
    Battery,
    Button,
    Configuration,
    Lamp,
    MagneticSensor,
    MotionSensor,
    Motor,
    Reader,
    Sound,
)


class Toio:
    """The toio cube to control.
    For more information, please refer to https://toio.github.io/toio-spec/docs/ble_communication_overview.

    Args:
        address (str, optional): Bluetooth device address of toio in small letter.
            - Defaults to None.
        name (str, optional): Name of toio.
            - Defaults to None.
    """

    def __init__(self, address: str = None, name: str = None) -> None:
        self.__address = address
        self.__name = name
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
    def address(self) -> str:
        return self.__address

    @property
    def name(self) -> str:
        return self.__name

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
