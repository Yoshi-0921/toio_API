"""Source code for the JoyStickControl scenario class.
Users can asynchronously control toio cubes by multiple joystick controllers.
Currently, only DUALSHOCK3 (PS3 controller) is supported.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

import asyncio
import random
from typing import List

import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (600, 425)  # 画面サイズ (横/縦)
MAT_HEIGHT = 216
MAT_WIDTH = 304
MAT_HEIGHT_MIN = 142
MAT_WIDTH_MIN = 98
pygame.display.set_caption("window test")  # Windowタイトルの設定
X_CENTER = int(SCREEN_SIZE[0] / 2)
Y_CENTER = int(SCREEN_SIZE[1] / 2)

from toio_API.scenarios.abstract_scenario import AbstractScenario
from toio_API.utils.toio import Toio


class JoyStickControl(AbstractScenario):
    def __init__(self, toios: List[Toio]) -> None:
        super().__init__(toios)
        self.initialize_controller()

    def initialize_controller(self):
        pygame.init()
        pygame.joystick.init()

        joy = pygame.joystick.Joystick(0)
        self.num_axes = joy.get_numaxes()
        self.num_buttons = joy.get_numbuttons()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)  # SCREEN_SIZEの画面を作成
        mat_image = pygame.image.load("figs/normal_mat.png")
        self.mat_image = pygame.transform.scale(mat_image, SCREEN_SIZE)
        bullet_image = pygame.image.load("figs/bullet.jpeg")
        self.bullet_image = pygame.transform.scale(bullet_image, (50, 10))
        self.bullets = []

    async def _main(self, **kwargs):
        while True:
            await self.print_screen()

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
            self.bullets = []
            await toio.sound.play(sound_effect=10)
        elif button_status[11]:  # R1 button
            self.bullets.append(self.bullet_image)
            await toio.sound.play(sound_effect=random.randint(0, 10))

        elif button_status[12]:  # △ button
            toio.forward_speed = 150
            await toio.lamp.turn_on(time=1, red=255, green=0, blue=0)
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
            await toio.lamp.turn_on(time=1, red=0, green=0, blue=255)
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

    async def print_screen(self):
        joy = pygame.joystick.Joystick(0)
        self.screen.fill((0, 0, 0))  # 画面を黒色で塗りつぶす
        # self.screen.blit(self.mat_image, (0, 0))
        for bullet_image in self.bullets:
            self.screen.blit(bullet_image, (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])))
        # イベント処理
        for event in pygame.event.get():  # ×ボタンによる終了
            if event.type == QUIT:  # 終了イベント
                sys.exit()

        # ジョイスティック(アナログバー左スティック)状態の取得
        circle_x = int(
            (joy.get_axis(0) + 1) * X_CENTER
        )  # joystick(横軸)の方向キーはは-1～1の範囲で取得できる
        circle_y = int(
            (joy.get_axis(1) + 1) * Y_CENTER
        )  # joystick(縦軸)の方向キーはは-1～1の範囲で取得できる

        # 描画範囲の上下限チェック
        if circle_x < 0:
            circle_x = 0
        elif circle_x > SCREEN_SIZE[0]:
            circle_x = SCREEN_SIZE[0]

        if circle_y < 0:
            circle_y = 0
        elif circle_y > SCREEN_SIZE[1]:
            circle_y = SCREEN_SIZE[1]

        pygame.draw.circle(self.screen, (255, 0, 0), (circle_x, circle_y), 10)
        pygame.display.update()

        await asyncio.sleep(0.01)
