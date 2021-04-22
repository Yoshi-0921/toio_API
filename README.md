<div align="center">

<img src="https://user-images.githubusercontent.com/60799014/115414156-c4ded580-a230-11eb-899c-874fdd7702be.png" width="200px">


### Simple toio API for Python Users

---

<p align="center">
  <a href="https://toio.io/">Website</a> •
  <a href="#about">About</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#examples">Examples</a> •
  <a href="#customs">Customs</a> •
  <a href="https://toio.io/blog/detail/20210412_toioClub.html">Community</a> •
  <a href="https://github.com/Yoshi-0921/toio_API/blob/main/LICENSE">License</a>
</p>
</div>

## About
This is unofficial toio control API for python users. Suitable to handle asynchronous operations using several toio cubes. 

これはtoio好きのtoio好きによるtoio好きのための非公式APIです。Pythonで複数のtoioキューブを非同期制御したい方向けのライブラリです。

## How To Use
基本的に`$ python main.py`で実行できます。toioの行動パターンは実装した「シナリオ」に基づいており、例として以下の４つのシナリオを用意しています。

<p align="center">
  <a href="#spin">spin</a> •
  <a href="#run-and-spin">run_spin</a> •
  <a href="#chase">chase</a> •
  <a href="#collision-avoidance">collision_avoidance</a>
</p>

デフォルトでは`make_scenario(scenario_name='spin', ...)`が設定されていますが、その他のシナリオでtoioを制御したい場合は該当するシナリオ名に変更してください。

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
#### その他
- `asyncio.run(discover_toios())`: 接続可能なtoioを見つけます。発見できた場合、そのtoioのBLE_addressがリスト型で返されます。
- `create_toios(toio_addresses)`: 見つけたtoioのBLE_addresを基にtoio制御クラスを作成します。引数に名前も設定できます。
- `make_scenario(toios)`: toioの行動パターンを決めるシナリオを作成します。この時、自動的にtoioとのBLE通信が開始されます。
- `scenario.run()`:　作成したシナリオを実行します。　

## Examples
４つのシナリオの実装コードです。たったの数行のコードでtoioを簡単に制御できます。

### Spin
toioがグルグルとその場で回転して、5秒後に停止します。

```py
# scenarios/examples/spin.py

class Spin(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)
```

[Demo video clip](https://youtu.be/rINq-bm9uKI)

### Run and Spin
toioが１秒間走り、その後１秒間スピンします。

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

[Demo video clip](https://youtu.be/3fU0nKxnZRQ)

### Chase
2体以上のtoioが必要です。1体のtoioに目掛けてその他のtoioが追いかけます。

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

[Demo video clip](https://youtu.be/juGjJ5iSx_k)

### Collision Avoidance
2体のtoioが必要です。toioを互いの正面に向き合わせて実行します。初めに直進しますが、近づいたら衝突回避行動をします。

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

[Demo video clip](https://youtu.be/1LJGxODB4vM)

## Customs
自分のオリジナルコードでtoioを制御する場合、`scenarios/customs/`に用意したカスタムシナリオにコーディングしてください（Custom1 ~ Custom3まで実装できます）。完成したら`main.py`でシナリオ名を'custom1'に変更して実行してみましょう！

```
# scenarios/customs/custom1.py

class Custom1(AbstractSenario):
    async def _main(self):
        raise NotImplementedError()

```
