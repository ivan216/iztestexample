from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.dancing import partner
from rpze.structs.zombie import ZombieStatus
from random import randint
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

#有相位： 400 + 50 * 0.524 + 50 * 0.062 = 429
#无相位： 400 + 50 * 0.898 + 50 * 0.314 = 460.6（差）
#           450 第二鬼踩4或5路雷

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0 5-0
        .....
        .....
        .....
        pphtz
        tptzs
        mj 
        0  
        2-9''')
    
    h_r = [0] * 9
    _50_count = 0
    c = 0
    h_c = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50_count
        iz_test.game_board.sun_num = 2000
        mj = iz_test.game_board.zombie_list[0]
        t = iz_test.ground["5-3"]
        # mjc = 75   # 75 
        # iz_test.game_board.mj_clock = randint(mjc,mjc+10)
        await until(lambda _:mj.status is ZombieStatus.dancing_walking).after(460)
        await until(lambda _:iz_test.game_board.mj_clock%460==75).after(randint(0,10))
        mj2 = place("mj 5-9")

        await until(lambda _:mj2.status is ZombieStatus.dancing_summoning)
        wb = partner(mj2,"a")
        await until(lambda _:wb.is_dead)
        await until(lambda _:mj2.status is ZombieStatus.dancing_summoning)
        wb = partner(mj2,'a')
        await until(lambda _:wb.hp < 90)
        if not t.is_dead:
            place("xg 5-6")
            _50_count += 1

    @iz_test.on_game_end()
    def count(_):
        nonlocal c,h_c
        
        h = iz_test.ground["4-3"]
        if h is None:
            i = 0
        else:
            i = get_sunflower_remaining_sun(h) // 25
        h_r[i] += 1

        if i == 0:
            h_c += 1
        c += 1
        if c%10 == 0:
            print("收花率 %.4f"%(h_c/c))

    iz_test.start_test(jump_frame=0, speed_rate=1)
    print(h_r)
    print(_50_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)