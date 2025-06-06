from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
import matplotlib.pyplot as plt

# 171.5 >= dx*t >= 167.5
# 410

def fun(ctler: Controller):
    n = 1000
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        3-3 
        .....
        .....
        d_th.
        d_t..
        .....
        lz 
        0  
        3-6 ''')
    
    y = [.0] * n
    x = list(range(n))
    s = [.0] * n
    i = 0

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal i
        lz = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["3-4"]

        await until(lambda _:h.is_dead).after(4)
        speed = lz.dx
        lzx = lz.x
        ti1 = fm.time
        await until(lambda _:lz.is_dead)
        s[i] = lzx - lz.x
        ti = fm.time - ti1
        y[i] = speed * ti
        i += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    plt.scatter(x,y)
    plt.scatter(x,s,c='r')
    plt.show()

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)