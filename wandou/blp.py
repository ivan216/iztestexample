from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    iz_test = IzTest(game.controller).init_by_str('''
        500 -1
        3-0
        .....
        .....
        blphh
        .....
        .....
        gl 
        0  
        3-6''')
    
    xg_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        global xg_count
        zlist = iz_test.game_board.zombie_list
        plist = iz_test.ground
        gl = zlist[0]
        b = plist["3-1"]
        l = plist["3-2"]
        await until(lambda _:gl.accessories_hp_1<=0).after(randint(0,10))
        if l.hp >=160:
            place("xg 3-6")
            xg_count += 1
        else :
            await until(lambda _: gl.hp <= 170).after(randint(0,10))
            if b.hp >=300:
                place("xg 3-6")
                xg_count += 1
        
    iz_test.start_test(jump_frame=1, speed_rate=4)
    print(xg_count)
