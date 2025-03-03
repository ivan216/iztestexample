from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller

# 2-1-3 20k 134+95+84 = 0.0156
# 2-3-1 20k 102+107+114 = 0.016
# 对下路恐惧时间更长

# 3-2 20k 133+170 = 0.015
# 2-3 20k 214+101 = 0.0157

# 1-2-3 20k 227+54+103 = 0.019
# 3-2-1 20k >0.019
# 3-1-2 1-3-2 >0.02

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        20000 -1
        2-0 1-0 3-0
        xppxh
        xppxh
        xppxh
        .....
        .....
        tt tt tt 
        0  20 40  
        2-6 1-6 3-6 ''')
    
    _1fail = _2fail = _3fail = 0
    
    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal _1fail,_2fail,_3fail
        if not res:
            if iz_test.ground["1-0"] is not None:
                _1fail += 1
            if iz_test.ground["2-0"] is not None:
                _2fail += 1
            if iz_test.ground["3-0"] is not None:
                _3fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=3,print_interval=1e2)
    print(_1fail)
    print(_2fail)
    print(_3fail)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)