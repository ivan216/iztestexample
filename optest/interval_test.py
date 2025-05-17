from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
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
    
    no_pause_time = record = 0

    @iz_test.flow_factory.add_flow()
    async def _(_):
        iz_test.game_board.sun_num = 9876
        nonlocal no_pause_time,record

        await until(lambda _:iz_test.game_board.zombie_list.obj_num == 2)
        record = no_pause_time
        print("first zombie: ",no_pause_time)
        await until(lambda _:iz_test.game_board.zombie_list.obj_num == 3)
        print("second zombie: ",no_pause_time)
        print("interval: ", no_pause_time - record)

    @iz_test.flow_factory.add_tick_runner()
    def _(_):
        nonlocal no_pause_time
        if not ctler.read_bool(0x6a9ec0, 0x768, 0x164) :
            no_pause_time += 1
    
    @iz_test.on_game_end()
    def _(_):
        nonlocal no_pause_time,record
        no_pause_time = record = 0
        print()

    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(game_path) as game:
    fun(game.controller)