from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        dbl5o
        .....
        .....
        .....
        xt 
        0  
        2-2''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        star = iz_test.ground["2-4"]
        await delay(400)
        await until_plant_last_shoot(star).after(50)
        await repeat("cg 2-6")

    @iz_test.flow_factory.add_tick_runner()
    def check_end(fm:FlowManager):
        if iz_test.ground["2-0"] is None:
            return iz_test.end(True)
        if fm.time > 1000:
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)