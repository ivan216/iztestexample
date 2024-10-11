from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.iztest.cond_funcs import until_n_butter
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        y3_s_
        .....
        .....
        lz lz 
        0  20
        3-6 3-6''')
    
    _75_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        y = iz_test.ground["3-1"]
        l = iz_test.ground["3-2"]

        await until_n_butter(y,2)
        if l.is_dead :
            place("cg 3-6")
        else:
            place("lz 3-6")
        _75_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
