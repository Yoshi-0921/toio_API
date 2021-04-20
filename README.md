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
### Spin
````py
# -*- coding: utf-8 -*-

from scenarios import make_scenario
from utils.toio import Toio

if __name__ == '__main__':
    toio1 = Toio(name='Yoshi', address='B62DBD30-1D16-4796-A60F-E76903A3BEF0')
    toio2 = Toio(name='Moto', address='33139358-E12D-45F8-9B83-A23EBC3CDD58')
    scenario = make_scenario(scenario_name='spin', toios=[toio1, toio2])

    scenario.run()
````

## Examples
