from characteristics import (Battery, Button, Configuration, Lamp,
                             MotionSensor, Motor, Reader, Sound)


class Toio:
    def __init__(self):
        self.__battery = Battery()
        self.__button = Button()
        self.__lamp = Lamp()
        self.__motion_sensor = MotionSensor()
        self.__motor = Motor()
        self.__reader = Reader()
        self.__sound = Sound()
        self.__configuration = Configuration()

    @property
    def battery(self):
        return self.__battery

    @property
    def button(self):
        return self.__button

    @property
    def lamp(self):
        return self.__lamp

    @property
    def motion_sensor(self):
        return self.__motion_sensor

    @property
    def motor(self):
        return self.__motor

    @property
    def reader(self):
        return self.__reader

    @property
    def sound(self):
        return self.__sound

    @property
    def configuration(self):
        return self.__configuration


if __name__ == '__main__':
    t = Toio()
    print(t.button.uuid)
