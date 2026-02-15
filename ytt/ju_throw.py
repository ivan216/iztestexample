from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until,FlowManager
from rpze.iztest.operations import place
from rpze.structs.zombie import ZombieType

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        1000 -1
        3-1
        .....
        .....
        1....
        .....
        .....
        xg
        0
        1-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        zb = iz_test.ground.zombie(0)
        zb.die_no_loot()
        zb = iz_test.game_board.iz_place_zombie(2,8,ZombieType.gargantuar)
        zb.x = 400.01
        zb.hp = 1499
    
    iz_test.start_test(jump_frame=0, speed_rate=1, print_interval=100)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)