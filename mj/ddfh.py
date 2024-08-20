from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.plant_modifier import set_puff_x_offset
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus,Zombie
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager

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
        def _cond_func(fm: FlowManager):
            if mj.int_x > intx:
                iz_test.game_board.mj_clock = 230
                return False
            return True
        return AwaitableCondFunc(_cond_func)
    
    def keep_walking() ->AwaitableCondFunc:
        def _cond_func(fm: FlowManager):
            iz_test.game_board.mj_clock = 230
            return False
        return AwaitableCondFunc(_cond_func)
    
    three_fail = 0
    four_fail = 0
    five_fail = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        zlist = iz_test.game_board.zombie_list
        lz = zlist[0]
        plist = iz_test.ground
        pl = plist["1-2"]
        pl2 = plist["4-5"]
        # pl3 = plist["5-1"]
        # set_puff_x_offset(pl3,-5)

        await until(lambda _:pl2.hp <= 140)
        mj2 = place("mj 4-8")
        await walk_until_int_x(mj2,78)
        iz_test.game_board.mj_clock = 240   #239 ~ 258
        await delay(191)   # >=191 不发愣
        await keep_walking()

    @iz_test.on_game_end()
    def end_callback(result: bool):
        if not result:
            nonlocal three_fail,four_fail,five_fail
            if iz_test.game_board.griditem_list[2].id.rank != 0 :
                three_fail += 1
            if iz_test.game_board.griditem_list[3].id.rank != 0 :
                four_fail += 1
            if iz_test.game_board.griditem_list[4].id.rank != 0 :
                five_fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print("三路失败：",three_fail)
    print("四路失败：",four_fail)
    print("五路失败：",five_fail)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
