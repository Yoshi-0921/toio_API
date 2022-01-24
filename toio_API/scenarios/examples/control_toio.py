import asyncio
import random
from typing import List

import pygame
from toio_API.scenarios.abstract_scenario import AbstractSenario
from toio_API.utils.toio import Toio


class JoyControl(AbstractSenario):
    def __init__(self, toios: List[Toio]) -> None:
        super().__init__(toios)
        self.initialize_controller()

    def initialize_controller(self):
        pygame.init()
        pygame.joystick.init()

        joy = pygame.joystick.Joystick(0)
        self.num_axes = joy.get_numaxes()
        self.num_buttons = joy.get_numbuttons()

    async def _main(self, **kwargs):
        while True:
            axes_status, button_status = await self.press_button()
            await asyncio.gather(
                *[
                    self.__control(toio, axes_status[toio_id], button_status[toio_id])
                    for toio_id, toio in enumerate(self.toios)
                ]
            )
            await asyncio.sleep(0.01)

    async def __control(self, toio: Toio, axes_status, button_status):
        if button_status[0]:  # Select button
            await toio.sound.play(sound_effect=0)
        elif button_status[1]:  # Left stick
            await toio.sound.play(sound_effect=1)
        elif button_status[2]:  # Right stick
            await toio.sound.play(sound_effect=2)
        elif button_status[3]:  # Start button
            await toio.sound.play(sound_effect=3)
        elif button_status[4]:  # Up button
            await toio.sound.play(sound_effect=4)
        elif button_status[5]:  # Right button
            await toio.sound.play(sound_effect=5)
        elif button_status[6]:  # Down button
            await toio.sound.play(sound_effect=6)
        elif button_status[7]:  # Left button
            await toio.sound.play(sound_effect=7)
        elif button_status[8]:  # L2 button
            await toio.sound.play(sound_effect=8)
        elif button_status[9]:  # R2 button
            await toio.sound.play(sound_effect=9)
        elif button_status[10]:  # L1 button
            await toio.sound.play(sound_effect=10)
        elif button_status[11]:  # R1 button
            await toio.sound.play(sound_effect=random.randint(0, 10))

        elif button_status[12]:  # △ button
            toio.forward_speed = 150
            await toio.lamp.turn_on(time=15, red=255, green=0, blue=0)
            await toio.sound.play(sound_effect=1)

        elif button_status[13]:  # ○ button
            await toio.motor.control(
                left_speed=toio.forward_speed + int(min(-0.5, axes_status[0]) * 50),
                right_speed=toio.forward_speed - int(max(0.5, axes_status[0]) * 50),
            )

        elif button_status[14]:  # × button
            toio.forward_speed = 100
            await toio.motor.control(
                left_speed=toio.back_speed - int(min(-0.5, axes_status[0]) * 50),
                right_speed=toio.back_speed + int(max(0.5, axes_status[0]) * 50),
            )

        elif button_status[15]:  # □ button
            toio.forward_speed = 50
            await toio.lamp.turn_on(time=15, red=0, green=0, blue=255)
            await toio.sound.play(sound_effect=10)

        elif button_status[16]:
            await toio.sound.play(sound_effect=random.randint(0, 10))

        else:
            await toio.motor.control(left_speed=0, right_speed=0)

    async def press_button(self):
        joys = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        axes_status = [[joy.get_axis(i) for i in range(self.num_axes)] for joy in joys]
        button_status = [
            [joy.get_button(i) for i in range(self.num_buttons)] for joy in joys
        ]

        await asyncio.sleep(0.01)

        return axes_status, button_status
