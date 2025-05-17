from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.zombie import ZombieStatus
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.dancing import partner
from random import randint
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0 2-0
        dpwpt
        .ppt.
        p__hw
        .....
        .....
        mj 
        0  
        2-8''')
    
    _1_fail = _2_fail = _3_fail = 0
    _125_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _125_count
        wb_num = 0
        mj = iz_test.game_board.zombie_list[0]
        iz_test.game_board.mj_clock = randint(456,466)

        while wb_num < 3:
            await until(lambda _:mj.status is ZombieStatus.dancing_summoning)
            wb = partner(mj,"a")
            if wb is not None:
                wb_num += 1
                if wb_num < 3:
                    await until(lambda _:wb.is_dead)
        
        await until(lambda _:wb.status is not ZombieStatus.backup_spawning).after(4) #可以取2
        if wb.x < 86:
            if not wb.is_eating :
                place("xt 2-2")
                _125_count += 1
    
    @iz_test.on_game_end()
    def _(_):
        nonlocal _1_fail,_2_fail,_3_fail
        if iz_test.ground["1-0"] is not None:
            _1_fail += 1
        if iz_test.ground["2-0"] is not None:
            _2_fail += 1
        if iz_test.ground["3-0"] is not None:
            _3_fail += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_125_count)
    print("1失败 ",_1_fail)
    print("2失败 ",_2_fail)
    print("3失败 ",_3_fail)

with InjectedGame(game_path) as game:
    fun(game.controller)