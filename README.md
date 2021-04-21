<div align="center">

<img src="https://user-images.githubusercontent.com/60799014/115414156-c4ded580-a230-11eb-899c-874fdd7702be.png" width="200px">


### Toio API for Python Users

---

<p align="center">
  <a href="https://toio.io/">Website</a> •
  <a href="#about/">About</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#examples">Examples</a> •
  <a href="https://toio.io/blog/detail/20210412_toioClub.html">Community</a> •
  <a href="https://github.com/Yoshi-0921/toio_API/blob/main/LICENSE">License</a>
</p>
</div>

## About
This is unofficial Toio API for python users. Suitable to handle asynchronous operations using several toio cubes. 

これはToio好きのToio好きによるToio好きのための非公式APIです。Pythonで複数のToioを非同期制御したい方向けのパッケージです。

## How To Use
` $ python main.py`

```py
# main.py

import asyncio

from scenarios import make_scenario
from utils.general import create_toios, discover_toios

if __name__ == '__main__':
    toio_addresses = asyncio.run(discover_toios())
    toios = create_toios(toio_addresses=toio_addresses, toio_names=['Yoshi', 'Moto'])
    scenario = make_scenario(scenario_name='spin', toios=toios)

    scenario.run()
```

## Examples
### Spin
```py
# scenarios/examples/spin.py
class Spin(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)
```

![spin](https://user-images.githubusercontent.com/60799014/115505820-ff8a5180-a2b4-11eb-9e10-a9d84759ee95.gif)

### Run and Spin
```py
# scenarios/examples/run_spin.py
class RunSpin(AbstractSenario):
    async def _main(self):
        await asyncio.gather(*[self.__run_spin(toio) for toio in self.toios])

    async def __run_spin(self, toio: Toio):
        await toio.motor.control(left_speed=100, right_speed=100)
        await asyncio.sleep(1)
        await toio.motor.control(left_speed=-100, right_speed=100)
        await asyncio.sleep(1)
```
### Chase
```py
# scenarios/examples/chase.py
class Chase(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            response = await read_information(self.toios)
            await asyncio.gather(*[self.__chase(toio, toio_idx, **response) for toio_idx, toio in enumerate(self.toios)])
            await asyncio.sleep(0.1)

    async def __chase(self, toio: Toio, toio_idx: int, **kwargs):
        if toio_idx == 0:
            await toio.motor.acceleration_control(rotation_speed=90)
        else:
            await toio.motor.target_control(
                max_speed=50,
                x_coordinate=kwargs[self.toios[0].name]['center_x'],
                y_coordinate=kwargs[self.toios[0].name]['center_y']
            )
```
### Collision Avoidance
```py
# scenarios/examples/collision_avoidance.py
class CollisionAvoidance(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            response = await read_information(self.toios)
            await asyncio.gather(*[self.__chase(toio, toio_idx, **response) for toio_idx, toio in enumerate(self.toios)])
            await asyncio.sleep(0.01)

    async def __chase(self, toio: Toio, toio_idx: int, **kwargs):
        distance = math.dist(
            [kwargs[self.toios[0].name]['center_x'], kwargs[self.toios[0].name]['center_y']],
            [kwargs[self.toios[1].name]['center_x'], kwargs[self.toios[1].name]['center_y']]
        )
        if distance < 70:
            await toio.motor.control(-10, -10)
        else:
            await toio.motor.control(left_speed=50, right_speed=50)
```
