from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        y....
        .....
        .....
        tt
        0  
        3-6 ''')
    
    fail_count = 0
    y_fail_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        zlist = iz_test.game_board.zombie_list
        zb = zlist[0]
        zb.x = 780.0 + randint(0,40)

    @iz_test.on_game_end()
    def end_callback(result: bool):
        if not result:
            nonlocal fail_count,y_fail_count
            plist = iz_test.ground
            fail_count += 1
            if plist["3-1"] is not None:
                y_fail_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=1)
    print("失败次数：",fail_count)
    print("没吃掉玉米次数：",y_fail_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)