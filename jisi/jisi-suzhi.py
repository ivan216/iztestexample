from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        wdtzh
        dh__t
        .....
        .....
        .....
        xg mj
        0  300
        1-6 1-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        mjc = 63 
        iz_test.game_board.mj_clock = randint(mjc,mjc+10)
        await delay(300)
        mj = iz_test.game_board.zombie_list[0]
        
    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if fm.time > 300:
            if iz_test.ground["1-0"] is None \
                and iz_test.ground["2-0"] is None :
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    iz_test.start_test(jump_frame=1, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)   