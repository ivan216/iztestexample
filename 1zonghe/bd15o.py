from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot,until_plant_n_shoot
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        bd15s
        .....
        .....
        .....
        kg
        0  
        2-6''')
    
    ldie = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        kg = iz_test.ground.zombie(0)
        st = iz_test.ground["2-4"]
        await delay(randint(1,4))
        kg.x = 11

        await until_plant_n_shoot(st,13).after(25+randint(0,10)) #30
        cg = place("cg 2-6")
    
    @iz_test.on_game_end()
    def _(res):
        nonlocal ldie
        if not res:
            if iz_test.ground["2-3"] is not None:
                ldie += 1

    iz_test.start_test(jump_frame=1, speed_rate=1)
    print(ldie)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
