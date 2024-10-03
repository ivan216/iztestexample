from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0
        xxpph
        xppxh
        .....
        .....
        .....
        tt   
        0  
        2-6 ''')
    
    _50 = 0
    _75 = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        tt = iz_test.ground.zombie(0)
        await until(lambda _:tt.hp < 90)
        if iz_test.ground["2-0"] is not None:
            place("xg 2-6")
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50 ,_75
        xi = iz_test.ground["1-2"]
        p = iz_test.ground["1-3"]
        p2 = iz_test.ground["2-2"]
        tt = iz_test.ground.zombie(0)
        await until(lambda _:tt.x < 145)    #130-145
        # await until(lambda _:p2.hp < 225)   #225 7%
        lz = place("lz 1-6")

        await until(lambda _:lz.hp< 150)
        if not p.is_dead:
            await until(lambda _:p.is_dead or lz.hp<90)
            if not p.is_dead:
                place("cg 1-6")
                _75 += 1
            else:
                place("xg 1-6")
                _50 += 1
        elif not xi.is_dead:
            place("xg 1-6")
            _50 += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_50)
    print(_75)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)