from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0 2-0 3-0
        2bbhl
        2bphl
        bbbph
        .....
        .....
        tz mj 
        0  20
        2-6 2-6''')
    
    h1 = None
    h2 = None
    h1_record = [0 for i in range(0,9)]
    h2_record = [0 for i in range(0,9)]

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal h1,h2
        h1 = iz_test.ground["1-4"]
        h2 = iz_test.ground["3-5"]        

    @iz_test.on_game_end()
    def count_sun(_):
        i = get_sunflower_remaining_sun(h1) // 25
        h1_record[i] += 1
        i = get_sunflower_remaining_sun(h2) // 25
        h2_record[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=1)
    print("h1漏花情况 ",h1_record)
    print("h2漏花情况 ",h2_record)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)