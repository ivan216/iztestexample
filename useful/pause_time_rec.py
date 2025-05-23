from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-3
        .....
        .....
        .tt..
        .....
        .....
        cg 
        0  
        3-6 ''')

    no_pause_time = 0
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm):
        nonlocal no_pause_time
        if no_pause_time == 0 :
            print("不含暂停时间：",no_pause_time)
            print("真实时间",fm.time)
        else:
            print("\033[2A\r\033[K"+"不含暂停时间：",no_pause_time)
            print("\033[K"+"真实时间",fm.time)
        if not ctler.read_bool(0x6a9ec0, 0x768, 0x164) :
            no_pause_time += 1

    @iz_test.on_game_end()
    def _(_):
        nonlocal no_pause_time
        no_pause_time = 0
        print()

    iz_test.start_test(jump_frame=0, speed_rate=1) 

with InjectedGame(game_path) as game:
    fun(game.controller)