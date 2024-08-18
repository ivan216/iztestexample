from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller

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
    
    no_pause_time = record = 0
    last_len = now_len = 1

    @iz_test.flow_factory.add_tick_runner()
    def print_no_pause_time(_):
        iz_test.game_board.sun_num = 9876
        nonlocal no_pause_time,record,last_len,now_len
        last_len = now_len
        now_len = iz_test.game_board.zombie_list.obj_num
        if (now_len == 2) and (last_len == 1) :
            record = no_pause_time
            print("first zombie: ",no_pause_time)
        if (now_len == 3) and (last_len == 2) :
            print("second zombie: ",no_pause_time)
            print("interval: ", no_pause_time - record)
        if not ctler.read_bool(0x6a9ec0, 0x768, 0x164) :
            no_pause_time += 1
    
    @iz_test.on_game_end()
    def clean(_):
        nonlocal no_pause_time,record,last_len,now_len
        no_pause_time = record = 0
        last_len = now_len = 1
        print()

    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)