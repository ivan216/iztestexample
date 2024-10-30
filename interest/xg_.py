from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until, delay

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-2
        .....
        .....
        .s._s
        .....
        .....
        lz 
        0  
        3-6''')
    
    xg = None
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal xg
        dc = iz_test.ground["3-4"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:lz.x < 280)

        await until(lambda _:dc.status_cd <= 24 or 85<=dc.status_cd<=100 )   # 24-100-85
        xg = place("xg 3-6")
    
    @iz_test.on_game_end()
    def out(_):
        if xg.hp<50:
            print(xg.hp)

    iz_test.start_test(jump_frame=0, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)