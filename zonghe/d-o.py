from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot,until_plant_die
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowFactory
from rpze.structs.zombie import ZombieStatus
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        
        .....
        .....
        d...o
        .....
        .....
        xg 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        d = iz_test.ground["3-1"]

        await until_plant_last_shoot(d).after(115 + randint(0,10))  #120
        place("cg 3-6")

    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowFactory):
        if iz_test.ground["3-0"] is None:
            return iz_test.end(True)
        if fm.time > 2000:
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)