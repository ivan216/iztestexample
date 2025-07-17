from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.structs.zombie import ZombieStatus
from rpze.structs.plant import PlantType,Plant

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        4-3
        .....
        .....
        .....
        ..o..
        .....
        xt 
        0  
        3-3''')
    
    zb = None
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal zb
        zb = iz_test.game_board.zombie_list[0]
        iz_test.game_board.new_plant(1,4,PlantType.gloomshroom)
        iz_test.game_board.new_plant(1,0,PlantType.gloomshroom)
        iz_test.game_board.new_plant(2,2,PlantType.winter_melon)
    
    iz_test.start_test(jump_frame=0, speed_rate=1,print_interval=5e2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)