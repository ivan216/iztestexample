from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

# 250+75*0.25+150*0.1+50*0.05=286，很差

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        yby_l
        .....
        .....
        tt
        0   
        3-6 ''')
    
    _75_count = 0
    y1_count = 0
    clear_count = 0
    y1 = y2 = b =None
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count,y1,y2,b
        tt = iz_test.game_board.zombie_list[0]
        l = iz_test.ground["3-5"]
        y1 = iz_test.ground["3-1"]
        y2 = iz_test.ground["3-3"]
        b = iz_test.ground["3-2"]

        await until(lambda _:l.hp < 300)    #300
        kg = place("kg 3-6")
        await until(lambda _:kg.hp < 190)    #190 85% 0.24
        if not l.is_dead:
            lz = place("lz 3-6")
            _75_count += 1
        
    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal y1_count,clear_count
        if not res:
            if not y1.is_dead:
                y1_count += 1
            if y1.is_dead & y2.is_dead & b.is_dead :
                clear_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_75_count)
    print(y1_count)
    print(clear_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)