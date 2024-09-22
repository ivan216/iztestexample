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
        ...h.
        mj 
        0  
        1-9''')
    
    _75_count = 0
    can_bu = False
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count,can_bu
        can_bu = False
        mj = iz_test.game_board.zombie_list[0]
        wb_num = 0

        while wb_num < 4:
            await until(lambda _:mj.status is ZombieStatus.dancing_summoning)
            wb = partner(mj,"a")
            if wb is not None:
                wb_num += 1
                if wb_num < 4:
                    await until(lambda _:wb.is_dead)

        if mj.x >= 256: #256
            await until(lambda _:can_bu)
            place("cg 1-6")
            _75_count += 1

        elif mj.hp < 320: #有可能被打7豌豆
            await until(lambda _:can_bu)
            place("cg 1-6") 
            _75_count += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal can_bu
        h = iz_test.ground["1-4"]
        h2 = iz_test.ground["5-4"]
        await until(lambda _:h.is_dead)
        await until(lambda _:315 <= iz_test.game_board.mj_clock%460 <= 352).after(randint(0,10))
        mj2 = place("mj 5-6")
        await until(lambda _:h2.hp <= 236)
        can_bu = True

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
