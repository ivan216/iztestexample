from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0
        xssss
        sssss
        .....
        .....
        .....
        lz 
        0  
        2-6  ''')
    
    hp = [0] * 16
    lz = None
    full = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal lz,full
        lz0 = iz_test.game_board.zombie_list[0]
        await until(lambda _:lz0.x < 152).after(randint(0,10))
        lz = place("lz 1-6")
        full = lz.accessories_hp_1
    
    @iz_test.on_game_end()
    def count(_):
        i = (full - lz.accessories_hp_1) // 20
        hp[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(hp)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)