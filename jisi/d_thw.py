from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant
from rpze.structs.zombie import ZombieStatus

import numpy as np

x =np.linspace(0.37,0.23,15) 
y =np.array([457,465,477,489,505,521,537,557,577,597,621,645,673,701,733])-410
[a,b,c] = np.polyfit(x,y,2)
def quadr(x,a,b,c):
    return a*x**2 + b*x + c

def fun(ctler: Controller):
    n = 1000
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        3-1 
        .....
        .....
        d_th.
        .....
        .....
        lz 
        0  
        3-6 ''')

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        lz = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["3-4"]

        await until(lambda _:h.is_dead).after(4)
        speed = lz.dx
        t = round(quadr(speed,a,b,c))
        await delay(t)
        place("cg 3-6")

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)