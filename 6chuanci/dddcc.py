from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        dddcc
        .....
        .....
        lz
        0
        3-6
        ''')
    
    cg_count = 0
    can_end = False

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal cg_count,can_end
        can_end = False
        c4= iz_test.ground["3-4"]
        d2=iz_test.ground["3-2"]
        d3 = iz_test.ground["3-3"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:lz.hp<90)
        if not c4.is_dead:
            lz = place("lz 3-6")
            cg_count += 1
        await until(lambda _:lz.hp<90)

        await (until_plant_last_shoot(d2) | delay(250))
        cg = place("cg 3-6")
        cg_count+=1
        can_end = True
        await until(lambda _:cg.hp < 170)
        place("cg 3-6")
        cg_count += 1

    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if can_end:
            if iz_test.ground["3-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
             
    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(cg_count)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)