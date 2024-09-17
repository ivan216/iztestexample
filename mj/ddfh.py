from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.structs.zombie import Zombie
from rpze.flow.utils import AwaitableCondFunc

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0 3-0 5-0
        .s...
        .....
        bz.3w
        d__ts
        p...z
        lz 
        0  
        4-6''')
    
    def walk_until_int_x(mj :Zombie,intx :int = 40) -> AwaitableCondFunc:
        def _cond_func(_):
            if mj.int_x > intx:
                iz_test.game_board.mj_clock = 230
                return False
            return True
        return AwaitableCondFunc(_cond_func)
    
    three_fail = 0
    four_fail = 0
    five_fail = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        pl = iz_test.ground["4-5"]

        await until(lambda _:pl.hp <= 140)
        mj = place("mj 4-8")
        await walk_until_int_x(mj,78)
        iz_test.game_board.mj_clock = 240
        await delay(191)   # 不发愣
        await walk_until_int_x(mj,0)    #mj已经死亡，不过仍能让舞伴继续前进

    @iz_test.on_game_end()
    def end_callback(result: bool):
        nonlocal three_fail,four_fail,five_fail
        if not result: 
            if iz_test.ground["3-0"] is not None:
                three_fail += 1
            if iz_test.ground["4-0"] is not None:
                four_fail += 1
            if iz_test.ground["5-0"] is not None:
                five_fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print("三路失败：",three_fail)
    print("四路失败：",four_fail)
    print("五路失败：",five_fail)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
