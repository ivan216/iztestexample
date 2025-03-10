from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.flow import FlowManager
from rpze.iztest.operations import delay , place
from rpze.flow.utils import until

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        5-5
        .....
        .....
        .....
        .....
        ....t
        lz
        0  
        5-9''')
    
    spawned = 0

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        iz_test.game_board.sun_num = 9876
        nonlocal spawned
        await delay(randint(200,700))
        place("lz 2-6")
        spawned = fm.time
        print("spawn: ",fm.time)
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        await until(lambda _:iz_test.game_board.zombie_list.obj_num == 3)
        if fm.time - spawned - 1 >= 0:
            print("placed: ",fm.time)
            print("reaction",fm.time - spawned - 1) # 刚放下看不到，认为反应为再减1cs
        else:
            print("fail")
            
    @iz_test.on_game_end()
    def _(_):
        nonlocal spawned
        spawned = 0
        print()
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)