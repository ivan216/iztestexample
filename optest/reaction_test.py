from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.flow import FlowManager
from rpze.iztest.operations import delay , place

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-5
        ....t
        .....
        .....
        .....
        .....
        lz
        0  
        1-7''')
    
    spawned = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        nonlocal spawned
        await delay(randint(200,300))
        place("lz 2-6")
        spawned = fm.time
        print("spawn: ",fm.time)

    last_len = now_len = 1

    @iz_test.flow_factory.add_tick_runner()
    def print_time(fm:FlowManager):
        iz_test.game_board.sun_num = 9876
        nonlocal last_len,now_len,spawned
        last_len = now_len
        now_len = len(list(~iz_test.game_board.zombie_list))

        if (now_len == 3) and (last_len == 2) :
            print("placed: ",fm.time)
            print("reaction",fm.time - spawned - 1) # 刚放下看不到，认为反应为再减1cs

    @iz_test.on_game_end()
    def clean(_):
        nonlocal last_len,now_len,spawned
        last_len = now_len = 1
        spawned = 0
        print()
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)