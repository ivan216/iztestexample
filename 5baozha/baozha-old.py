from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.dancing import partner
from rpze.structs.zombie import ZombieStatus
from random import randint
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

# 5相位，不超过418=补50*(0.3+0.05)，无相位，直接4路425

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0 5-0
        .....
        .....
        .....
        tppzh
        tzpts
        mj 
        0  
        5-9''')
    
    _50_count = 0
    h_r = [0] * 9
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _50_count
        iz_test.game_board.sun_num = 2000
        mj = iz_test.game_board.zombie_list[0]
        p = iz_test.ground["5-3"]
        mjc = 345   #345 83%
        iz_test.game_board.mj_clock = randint(mjc,mjc+10)
        wb_num = 0

        while wb_num < 3:
            await until(lambda _:mj.status is ZombieStatus.dancing_summoning)
            wb = partner(mj,"a")
            if wb is not None:
                wb_num += 1
                if wb_num < 3:
                    await until(lambda _:wb.is_dead)
        
        await until(lambda _:wb.status is not ZombieStatus.backup_spawning).after(4)
        if wb.x < 156 or 156<= wb.x <= 165 and not wb.is_eating:
            await until(lambda _:mj.hp < 280)   #280
            if not mj.is_eating:
                place("xg 5-6")
                _50_count += 1

    @iz_test.on_game_end()
    def _(_):
        i = get_sunflower_remaining_sun(iz_test.ground["4-5"]) // 25
        h_r[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=10)
    print(_50_count)
    print(h_r)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)