from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until,delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus
from random import randint

# 300.5,万分之2补鬼障杆，千分之4补双杆

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-3 3-4
        .....
        .....
        dyloz
        .....
        .....
        kg 
        0  
        3-6''')
    
    l_fail = y_fail = yl_fail = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        kg = iz_test.game_board.zombie_list[0]
        o = iz_test.ground["3-4"]
        l = iz_test.ground["3-3"]
        y = iz_test.ground["3-2"]
        o.hp = 4

        await until(lambda _:kg.accessories_hp_1 == 80).after(40)
        if kg.accessories_hp_1 == 60:
            await until(lambda _:kg.accessories_hp_1 == 0).after(20) # 20
        else:
            await until(lambda _:kg.hp == 250).after(0) #10
        place("xt 3-3")

        @iz_test.on_game_end()
        def check(_):
            nonlocal l_fail,y_fail,yl_fail
            if (not l.is_dead) and (not y.is_dead):
                yl_fail += 1
            elif not l.is_dead :
                l_fail += 1
            elif not y.is_dead:
                y_fail += 1
            
    iz_test.start_test(jump_frame=1, speed_rate=1)
    print(yl_fail)
    print(l_fail)
    print(y_fail)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)