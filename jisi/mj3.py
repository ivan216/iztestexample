from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.dancing import partner
from rpze.structs.zombie import ZombieStatus
from random import randint
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0 2-0
        ppzht
        dpptz
        .....
        .....
        .....
        mj 
        0  
        1-9''')
    
    _75_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        mj = iz_test.game_board.zombie_list[0]
        z = iz_test.ground["2-5"]
        wb_num = 0

        while wb_num < 4:
            await until(lambda _:mj.status is ZombieStatus.dancing_summoning)
            wb = partner(mj,"a")
            if wb is not None:
                wb_num += 1
                if wb_num < 4:
                    await until(lambda _:wb.is_dead)

        if mj.x >= 256: #256
            place("cg 1-6")
            _75_count += 1
        elif mj.hp < 320: #有可能被打7豌豆
            place("cg 1-6") 
            _75_count += 1

    iz_test.start_test(jump_frame=0, speed_rate=10)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
