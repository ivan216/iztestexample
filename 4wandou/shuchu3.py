from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.flow.flow import FlowManager
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 4-0 5-0
        2bbhl
        2bphl
        bbbph
        2bphl
        2bbhl
        tz 
        0  
        2-6''') # (25*0.08+50*0.2+0.02*25+0.03*50+75*0.62)+(25*0.28+50*0.3+75*0.02) = 84
    
    h1 = h2 = h3 = l1 = mj = mj2 = None
    h1_ = [0 for _ in range(9)]
    h1_l = [0 for _ in range(9)]
    h2_ = [0 for _ in range(9)]
    h3_ = [0 for _ in range(9)]

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal h1,h2,h3,l1,mj,mj2
        h1 = iz_test.ground["1-4"]
        h2 = iz_test.ground["5-4"]
        h3 = iz_test.ground["3-5"]
        l1 = iz_test.ground["1-5"]
        plant = iz_test.ground["4-5"]

        await delay(20)
        mj = place("mj 2-6")
        await until(lambda _:mj.status is ZombieStatus.dancing_walking ).after(100)
        await until(lambda _:iz_test.game_board.mj_clock % 460 == 80) #80 99%
        place("tz 4-6")
        await until(lambda _:plant.hp < 80)
        mj2 = place("mj 4-6")

    @iz_test.on_game_end()
    def end_callback(_):
        i = get_sunflower_remaining_sun(h1) // 25
        if l1.is_dead :
            h1_[i] += 1
        else:
            h1_l[i] += 1
        
        i = get_sunflower_remaining_sun(h2) // 25
        h2_[i] += 1
        i = get_sunflower_remaining_sun(h3) // 25
        h3_[i] += 1

    @iz_test.flow_factory.add_tick_runner()
    def check_end(_):
        nonlocal mj,mj2
        if (mj is not None) and (mj2 is not None) \
            and (mj.x < 200) and (mj2.x < 200):
            mj = mj2 = None
            return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print("h1无裂荚 ",h1_)
    print("h1有裂荚 ",h1_l)
    print("h2无裂荚 ",h2_)
    print("h3漏 ",h3_)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)