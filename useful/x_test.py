from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        .....
        bs...
        .....
        .....
        gl 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        zlist = iz_test.game_board.zombie_list
        zb = zlist[0]
        await until(lambda _: zb.int_x <= 120)
        place("cg 3-6")
    
    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    