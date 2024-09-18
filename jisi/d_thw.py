from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
import numpy as np

x =np.linspace(0.23,0.37,15) 
y =np.array([733,701,673,645,621,597,577,557,537,521,505,489,477,465,457])-410
[a,b,c] = np.polyfit(x,y,2)
def quadratic(x,a,b,c):
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
    async def place_zombie(_):
        lz = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["3-4"]

        await until(lambda _:h.is_dead).after(4)
        speed = lz.dx
        ti = round(quadratic(speed,a,b,c))
        await delay(ti)
        place("cg 3-6")

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)