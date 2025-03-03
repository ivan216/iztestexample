from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.plant import PlantStatus
from random import randint

# 24%成功率

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        dpwpt
        .....
        .....
        xg 
        0  
        3-7 ''')
    
    w = None
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal w
        p = iz_test.ground["3-4"]
        w = iz_test.ground["3-3"]
        await until_plant_last_shoot(p)
        place("xg 3-6")

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 500:
            if w.status is PlantStatus.squash_look:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)