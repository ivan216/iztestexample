from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until,delay
from rpze.iztest.operations import place
from random import randint
from rpze.flow.flow import FlowManager
from rpze.iztest.cond_funcs import until_plant_last_shoot, until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        spptz
        .....
        .....
        .....
        xg 
        0  
        2-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        p = iz_test.ground["2-3"]
        z = iz_test.ground["2-5"]

        await (until_plant_last_shoot(p) | delay(300))
        lz = place("lz 2-6")
        await until(lambda _:z.hp < 80)
        await until_plant_n_shoot(p).after(40)
        place("xg 2-6")
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 300:
            if iz_test.ground["2-1"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    iz_test.start_test(jump_frame=1,speed_rate=10)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)