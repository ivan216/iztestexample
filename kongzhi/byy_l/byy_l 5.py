from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until, delay
from rpze.rp_extend import Controller
from random import randint

## 200+ 50*0.654 + 75*0.46 = 267，最优解2

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-0
        .....
        .....
        byy_l
        .....
        .....
        lz 
        0  
        3-6''')
    
    _75_count = 0
    _50_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count,_50_count
        l = iz_test.ground["3-5"]
        b = iz_test.ground["3-1"]
        lz = iz_test.game_board.zombie_list[0]

        await (until(lambda _:lz.hp < 90) | until(lambda _:l.is_dead))
        if l.is_dead :
            _50_count += 1
            return iz_test.end(True)
        
        kg = place("kg 3-6")
        await until(lambda _: b.hp < 300 ) #300 90%
        
        while not l.is_dead:
            lz = place("lz 3-6")
            _75_count += 1
            await until(lambda _:lz.hp < 90) | until(lambda _:l.is_dead)
        
        await until(lambda _:lz.hp < 90)
        place("cg 3-6")
        _75_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_50_count)
    print(_75_count)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)