<div align="center">

<img src="https://user-images.githubusercontent.com/60799014/115414156-c4ded580-a230-11eb-899c-874fdd7702be.png" width="200px">


### Toio API for Python Users

---

<p align="center">
  <a href="https://toio.io/">Website</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#examples">Examples</a> •
  <a href="https://toio.io/blog/detail/20210412_toioClub.html">Community</a> •
  <a href="https://github.com/Yoshi-0921/toio_API/blob/main/LICENSE">License</a>
</p>
</div>

## How To Use

## Examples
### Spin
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
```py
# scenarios/examples/spin.py

import asyncio

from scenarios.abstract_scenario import AbstractSenario


class Spin(AbstractSenario):
    async def _main(self):
        for _ in range(50):
            await asyncio.gather(*[toio.motor.control() for toio in self.toios])
            await asyncio.sleep(0.1)

```
