from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        3-2
        .....
        .....
        b2hhl
        .....
        .....
        kg 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        zlist = iz_test.game_board.zombie_list
        plist = iz_test.ground
        kg = zlist[0]
        b = plist["3-1"]
        await (until(lambda _: kg.hp <= 230).after(45 + randint(0,10)) 
               | until(lambda _: b.hp <= 4))
        place("lz 3-6")
    
    row_three_fail_count = 0

    @iz_test.on_game_end()
    def end_callback(result: bool):
        if not result:
            nonlocal row_three_fail_count
            plant_list = iz_test.game_board.plant_list
            if plant_list["3-2"] is not None:
                row_three_fail_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=2)
    print(row_three_fail_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)