from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

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
    

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        zlist = iz_test.game_board.zombie_list
        tt = zlist[0]
        plist = iz_test.ground
        l = plist["3-5"]

        await until(lambda _:l.hp < 300)    #300
        kg = place("kg 3-6")

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
