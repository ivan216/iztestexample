from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        
        ..._.
        .....
        .....
        .....
        ..5..
        lz 
        0  
        5-2''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        star = iz_test.ground["5-3"]
        lz = iz_test.game_board.zombie_list[0]
        lz.accessories_hp_1 = 0
        lz.hp = 90

        await until_plant_last_shoot(star).after(80 + randint(0,10))   #80
        xg = place("xg 1-6")

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 800:
            if iz_test.ground["1-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)