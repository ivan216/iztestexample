from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.flow.flow import FlowManager
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0 3-0 4-0 
        .....
        2bphl
        bbbph
        2bphl
        .....
        lz 
        0  
        3-6''')
    
    # b = None
    # mj = None
    h1 = None
    h2 = None
    h1_record = [0 for _ in range(9)]
    h2_record = [0 for _ in range(9)]

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal h1,h2   #,b,mj
        # lz = iz_test.game_board.zombie_list[0]
        # b = iz_test.ground["3-1"]
        h1 = iz_test.ground["2-4"]
        h2 = iz_test.ground["4-4"]
        h = iz_test.ground["3-5"]

        await until(lambda _:h.is_dead)
        mj = place("mj 3-6")
        await delay(20)
        place("cg 3-6")

    @iz_test.on_game_end()
    def end_callback(_):
        i = get_sunflower_remaining_sun(h1) // 25
        h1_record[i] += 1
        i = get_sunflower_remaining_sun(h2) // 25
        h2_record[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print("h1漏花情况 ",h1_record)
    print("h2漏花情况 ",h2_record)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)