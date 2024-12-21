from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun
from rpze.iztest.dancing import partner
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0 3-0 4-0
        .....
        blpsh
        .._._
        yby_l
        .....
        mj
        0  
        3-6 ''')
    
    #byy_l 
    #yby_l
    
    _50_count = _300_count = _225_count =  0
    tz_fail = tou_fail = nobu_fail = 0
    sun_no = [0] * 9
    buti = butou = nobu = False

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50_count,_300_count,_225_count,buti,butou,nobu
        buti = butou = nobu = False
        mj = iz_test.game_board.zombie_list[0]
        mjc = iz_test.game_board.mj_clock % 460
        
        await until(lambda _:mj.status is ZombieStatus.dancing_walking ).after(50)
        if mjc <= 440 and mjc >= 160:   #160-440
            await (until(lambda _:mj.hp < 170) | until(lambda _:mj.x < 140))    #140
            if mj.hp < 170:
                place("tz 4-6")
                _300_count += 1
                place("tz 2-6")
                buti = True
            else:
                wb = partner(mj,"w")
                if (wb is not None) and (wb.hp >= 170):
                    place("xg 2-6")
                    _50_count += 1
                else : 
                    if (wb is not None):
                        await until(lambda _:wb.is_dead)
                    await until(lambda _:mj.status == ZombieStatus.dancing_summoning).after(200)
                    place("xg 2-6")
                    _50_count += 1
                nobu = True
        else:
            await repeat("xg 2-6")
            await delay(250)    #250
            place("xt 3-3")
            _225_count += 1
            butou = True

    @iz_test.on_game_end()
    def count_sun(res:bool):
        nonlocal tz_fail,tou_fail,nobu_fail
        if iz_test.ground["2-5"] is None:
            i = 0
        else:
            h = iz_test.ground["2-5"]
            i = get_sunflower_remaining_sun(h) // 25

        if buti :
            if not res:
                tz_fail += 1
        if butou :
            if not res:
                tou_fail += 1
        if nobu :
            sun_no[i] += 1
            if not res:
                nobu_fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print("补50：",_50_count)
    print("补50死亡：",nobu_fail)
    print("补50花剩余：",sun_no)
    print()

    print("补300：",_300_count)
    print("补梯死亡：",tz_fail)
    print()

    print("补225：",_225_count)
    print("补偷死亡：",tou_fail)
    print()


with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)