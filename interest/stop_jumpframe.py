from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place
from rpze.flow.utils import until
from random import randint
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        bphl2
        .....
        .....
        kg 
        0  
        3-6''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        b = iz_test.ground["3-1"]
        await until(lambda _: b.hp <= 220).after(randint(0,10)) 
        place("cg 3-6")

    @iz_test.flow_factory.add_flow()
    async def _(_):
        kg = iz_test.game_board.zombie_list[0]
        await until(lambda _: not kg.is_not_dying)

        print(f"current test: {iz_test._test_time + 1}")
        ctler.end_jump_frame()
        iz_test.game_board.frame_duration = 5
    
    @iz_test.on_game_end()
    def _(_):
        ctler.start_jump_frame()
    
    iz_test.start_test(jump_frame=1, speed_rate=0.01)

with InjectedGame(game_path) as game:
    fun(game.controller)