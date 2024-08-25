from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until, delay
from rpze.rp_extend import Controller
from random import randint

## 200 + 50*0.62 + 75*0.47 + 50*0.008 = 266.7 最优

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-0
        .....
        .....
        yby_l
        .....
        .....
        lz 
        0  
        3-6''')
    
    _75_count = 0
    _50_count = 0
    _175_count = 0
    y1_count = 0
    clear_count = 0
    y1 = y2 = b = None
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count,_50_count,y1,y2,b,_175_count
        l = iz_test.ground["3-5"]
        y1 = iz_test.ground["3-1"]
        b = iz_test.ground["3-2"]
        y2 = iz_test.ground["3-3"]
        lz = iz_test.game_board.zombie_list[0]

        await (until(lambda _:lz.hp < 90) | until(lambda _:l.is_dead))
        if l.is_dead :
            _175_count += 1
            return iz_test.end(True)
        
        kg = place("kg 3-6")
        await until(lambda _: y1.hp < 20 ) #20 90%
        while not l.is_dead:
            lz = place("lz 3-6")
            _75_count += 1
            await (until(lambda _:lz.hp < 90) | until(lambda _:l.is_dead))
        
        await until(lambda _:lz.hp < 90)
        if not y1.is_dead:
            await repeat("cg 3-6")
            _75_count += 2
        elif (not y2.is_dead) | (not b.is_dead):
            place("cg 3-6")
            _75_count += 1
        else:
            place("xg 3-6")
            _50_count += 1

    @iz_test.on_game_end()
    def check(res:bool):
        nonlocal y1_count,clear_count
        if not res:
            if not y1.is_dead:
                y1_count += 1
            if y1.is_dead & y2.is_dead & b.is_dead :
                clear_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_175_count)
    print(_75_count)
    print(_50_count)
    print(y1_count)
    print(clear_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)