from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.zombie import ZombieStatus

import matplotlib.pyplot as plt

def fun(ctler: Controller):
    n = 10000
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
    
    x = [.0] * n
    y = [0] * n
    max_cg_time = 0
    i = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        lz = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["3-4"]

        await until(lambda _:h.is_dead).after(4)
        x[i] = lz.dx
        ti = fm.time
        await until(lambda _:lz.is_dead)
        y[i] = fm.time - ti

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        nonlocal max_cg_time
        cg = place("cg 4-6")
        await until(lambda _:cg.status is ZombieStatus.pole_vaulting_jumping)
        if fm.time > max_cg_time:
            max_cg_time = fm.time
    
    @iz_test.on_game_end()
    def plus_i(_):
        nonlocal i
        i += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(max_cg_time)
    plt.scatter(x,y,marker='.')
    plt.xlabel("speed")
    plt.ylabel("time")
    plt.show()

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)