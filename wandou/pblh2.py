from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        2000 -1
        3-0
        .....
        .....
        pblh2
        .....
        .....
        tz xg
        0  20
        3-6 3-6                       
        ''') # 200 + 0.2*50 + 0.03*75
    # tz xg 78-81%

    xg_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal xg_count
        tz = iz_test.game_board.zombie_list[0]
        p = iz_test.ground["3-1"]
        b = iz_test.ground["3-2"]
        await until(lambda _:tz.accessories_hp_2 < 1)
        if tz.x > 162:
            await until(lambda _:tz.hp < 350)  #350 
            place("xg 3-6")
            xg_count += 1

    # @iz_test.flow_factory.add_tick_runner()
    # def check(fm:FlowManager):
    #     if iz_test.ground["3-0"] is None:
    #         return iz_test.end(True)
    #     if fm.time >0:
    #         if iz_test.game_board.zombie_list.obj_num == 0:
    #             return iz_test.end(False)

    # @iz_test.on_game_end()
    # def result(res):
    #     if not res:
    #         print("fail:",tz_x)
    #     else:
    #         print("success:",tz_x)

    iz_test.start_test(jump_frame=0, speed_rate=5)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
