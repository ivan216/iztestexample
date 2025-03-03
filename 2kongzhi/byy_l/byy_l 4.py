from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

## 250+75*0.2 + 75*0.025 +50*0.008 = 267.2，稍差

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-0
        .....
        .....
        byy_l
        .....
        .....
        tt  
        0   
        3-6 ''')
    
    _75_count = 0
    _50_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count,_50_count
        l = iz_test.ground["3-5"]
        tt = iz_test.game_board.zombie_list[0]

        await until(lambda _:l.hp < 270)    #270
        kg = place("kg 3-6")
        await until(lambda _:kg.hp < 190)    #190
        if not l.is_dead:
            place("lz 3-6")
            _75_count += 1
        
    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal _50_count
        if not res:
            if (iz_test.ground["3-2"] is None) & (iz_test.ground["3-3"] is None) :
                _50_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_75_count)
    print(_50_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)