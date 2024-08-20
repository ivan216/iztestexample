from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        byy_l
        .....
        .....
        lz 
        0  
        3-6''')
    
    _75_count =0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        l = iz_test.ground["3-5"]
        b = iz_test.ground["3-1"]
        lz = iz_test.game_board.zombie_list[0]
        
        while not l.is_dead:
            await (until(lambda _:lz.hp < 90) | until(lambda _:l.is_dead))
            if not l.is_dead :
                lz = place("lz 3-6")
                _75_count += 1

        await (until(lambda _:lz.hp <= 110) | until(lambda _:lz.int_x <= 320))
        cg1 = place("cg 3-6")
        await delay(20)
        cg2 = place("cg 3-6")
        _75_count += 2

        await (until(lambda _:cg1.butter_cd > 0) | until(lambda _:cg2.butter_cd >0))
        if cg1.butter_cd > 0 :
            if (cg1.int_x > 270) & (cg1.int_x < 300):
                place("cg 3-6")
                _75_count += 1
            elif cg1.int_x >= 300:
                await until(lambda _:cg2.butter_cd >0)
                place("cg 3-6")
                _75_count += 1
        elif cg2.butter_cd > 0 :
            if  (cg2.int_x > 270) & (cg2.int_x < 300):
                place("cg 3-6")
                _75_count += 1
            elif cg2.int_x >= 300:
                await until(lambda _:cg1.butter_cd >0)
                place("cg 3-6")
                _75_count += 1
        else:
            await (until(lambda _:cg1.hp < 170) | until(lambda _:cg2.hp < 170))
            if cg1.hp < 170:
                await until(lambda _:cg2.hp < 170)
                await repeat("cg 3-6")
                _75_count += 2
            else :
                await until(lambda _:cg1.hp < 170)
                await repeat("cg 3-6")
                _75_count += 2

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
