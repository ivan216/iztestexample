from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from random import randint

# 2-3-1 45-47-56
# 1-2-3 71-39-32


def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        2-0 3-0
        .....
        xppxh
        xppxh
        .....
        .....
        tt tt   
        0  20   
        2-6 3-6 ''')
    
    _2fail = _3fail = 0
    
    @iz_test.on_game_end()
    def count(res:bool):
        nonlocal _2fail,_3fail
        if not res:
            if iz_test.ground["2-0"] is not None:
                _2fail += 1
            if iz_test.ground["3-0"] is not None:
                _3fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_2fail)
    print(_3fail)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)