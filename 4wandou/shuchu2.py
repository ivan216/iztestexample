from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        5-4
        2bbhl
        2bphl
        bbbph
        2bphl
        2bbhl
        tz 
        0  
        2-6''') #滑5列，漏花（75*0.67+50*0.29+50*0.03）+（75*0.12+25*0.07+50*0.79）= 118
    
    h1 = h2 = l1 = l2 = mj2= None
    h1_ = [0 for _ in range(9)]
    h2_ = [0 for _ in range(9)]
    h1_l = [0 for _ in range(9)]
    h2_l = [0 for _ in range(9)]

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal h1,h2,l1,l2,mj2
        h1 = iz_test.ground["1-4"]
        h2 = iz_test.ground["5-4"]
        l1 = iz_test.ground["1-5"]
        l2 = iz_test.ground["5-5"]

        await delay(20)
        mj = place("mj 2-6")
        await until(lambda _:mj.status is ZombieStatus.dancing_walking ).after(100)
        await until(lambda _:iz_test.game_board.mj_clock % 460 == 380) # 380
        place("tz 4-6")
        await delay(20)
        mj2 = place("mj 4-6")

    @iz_test.on_game_end()
    def _(_):
        i = get_sunflower_remaining_sun(h1) // 25
        if l1.is_dead :
            h1_[i] += 1
        else:
            h1_l[i] += 1
        
        i = get_sunflower_remaining_sun(h2) // 25
        if l2.is_dead :
            h2_[i] += 1
        else:
            h2_l[i] += 1

    @iz_test.flow_factory.add_tick_runner()
    def _(_):
        nonlocal mj2
        if (mj2 is not None) and mj2.x < 200:
            mj2 = None
            return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print("h1无裂荚 ",h1_)
    print("h1有裂荚 ",h1_l)
    print("h2无裂荚 ",h2_)
    print("h2有裂荚 ",h2_l)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)