from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.iztest.cond_funcs import until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        2-1
        .....
        s5p5_
        .....
        .....
        .....
        lz 
        0  
        2-6''')
    
    _50_count = 0
    _75_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50_count,_75_count
        zlist = iz_test.game_board.zombie_list
        lz = zlist[0]
        plist = iz_test.ground
        star = plist["2-2"]
        star2 = plist["2-4"]
        p = plist["2-3"]
        while not star2.is_dead:
            await (until(lambda _:lz.hp < 90) | until(lambda _:star2.is_dead))
            if not star2.is_dead:
                lz = place("lz 2-6")
                _75_count += 1

        await (until(lambda _:lz.hp <90) | until(lambda _:p.is_dead))
        if not p.is_dead:
            place("cg 2-6")
            _75_count += 1
        elif lz.hp < 90 & p.is_dead:
            place("lz 2-6")
            _75_count += 1
        else:
            await until_plant_n_shoot(star,1).after(40)
            if lz.hp < 90:
                place("lz 2-6")
                _75_count += 1
            else:
                await until_plant_n_shoot(star,1).after(40)
                if lz.hp < 90:
                    await delay(50)
                    place("xg 2-6")
                    _50_count += 1
                
        
    iz_test.start_test(jump_frame=1, speed_rate=5)
    print("50数：",_50_count)
    print("75数：",_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)