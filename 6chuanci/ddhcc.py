from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        ddhcc
        .....
        .....
        lz 
        0  
        3-6''')
    
    d_die_h = [0] * 9
    d_alive_h = [0] * 9

    @iz_test.flow_factory.add_flow()
    async def _(_):
        lz = iz_test.game_board.zombie_list[0]
        c = iz_test.ground["3-4"]
        d = iz_test.ground["3-2"]

        await until_plant_last_shoot(d).after(randint(0,10))
        place("cg 3-6")
    
    @iz_test.on_game_end()
    def _(res:bool):
        h = iz_test.ground["3-3"]
        i = get_sunflower_remaining_sun(h)//25

        if res: #漏花实际上就这两种情况
            d_die_h[i] += 1
        else:
            d_alive_h[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=2)
    print("撑杆存活漏花 ",d_die_h)
    print("大喷存活漏花 ",d_alive_h)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)