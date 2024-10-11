from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.dancing import partner
from rpze.iztest.cond_funcs import until_plant_n_shoot

# 1035

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        1-0 2-0 3-0 4-0 5-0
        dwptz
        .ppts
        p__hw
        dtp_s
        dpwpt
        lz 
        0  
        4-6''')
    
    _1_fail = _2_fail = _3_fail = _4_fail = _52_fail = _52_suc = 0
    _50_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50_count
        t_die = False
        d = iz_test.ground["4-1"]
        p = iz_test.ground["2-2"]
        t = iz_test.ground["2-4"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:lz.x < 310)    #310
        await until_plant_n_shoot(d).after(33 + randint(0,10))
        mj = place("mj 4-6")
        await until(lambda _:mj.status is ZombieStatus.dancing_summoning).after(400) #判断相位时间

        await until(lambda _:iz_test.game_board.mj_clock%460 == 242).after(randint(0,10))
        mj2 = place("mj 2-9")

        await until(lambda _:mj2.status is ZombieStatus.dancing_summoning)
        wb = partner(mj2,"a")
        await until(lambda _:wb.hp < 90)
        if not t.is_dead:
            await delay(25) #反应时间
            place("xg 2-6")
            _50_count += 1
        else:
            t_die = True
        
        for _ in range(2):      #一直到第二只前舞伴
            await until(lambda _:wb is None or wb.is_dead)
            while wb is None or wb.is_dead:
                await until(lambda _:mj2.status is ZombieStatus.dancing_summoning)
                wb = partner(mj2,"a")

        if t_die:
            await until(lambda _:wb.status != ZombieStatus.backup_spawning).after(4)
            if wb.x < 166:
                if not wb.is_eating :
                    place("xg 2-6")
                    _50_count += 1

        await until(lambda _:wb.hp < 90)
        place("xg 2-6")
        _50_count += 1

    @iz_test.on_game_end()
    def count(res:bool):
        nonlocal _1_fail,_2_fail,_3_fail,_4_fail,_52_fail,_52_suc
        if iz_test.ground["1-0"] is not None:
            _1_fail += 1
        if iz_test.ground["2-0"] is not None:
            _2_fail += 1
        if iz_test.ground["3-0"] is not None:
            _3_fail += 1
        if iz_test.ground["4-0"] is not None:
            _4_fail += 1
        if iz_test.ground["5-0"] is not None:
            if iz_test.ground["5-2"] is None:
                _52_suc += 1
            else:
                _52_fail += 1
    
    iz_test.start_test(jump_frame=0, speed_rate=1)
    print("1补(75) ",_1_fail)
    print("2补(75) ",_2_fail)
    print("3补(75) ",_3_fail)
    print("4补(75) ",_4_fail)
    print("5补(175) ",_52_fail)
    print("5补(125) ",_52_suc)
    print("50数 ",_50_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)