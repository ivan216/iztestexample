from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-1
        t....
        .....
        ...c.
        bl...
        .....
        lz 
        0  
        1-6 ''')
    
    no_pause_time = record = 0

    # 0cs放置僵尸 -> 1cs僵尸出现在场上 -> 2cs磁铁cd变成1500
    # 外置节拍器，bpm 92，数14拍，非常准确

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal no_pause_time,record
        iz_test.game_board.sun_num = 9876
        c = iz_test.ground["3-4"]

        await until(lambda _:c.status_cd == 1500)
        record = no_pause_time
        print("magnet activated: ",no_pause_time)
        await until(lambda _:iz_test.game_board.zombie_list.obj_num == 3)
        print("kg placed: ",no_pause_time)
        print("equal interval(912-915 is good): ",no_pause_time - record + 2)
        print("magnet cd left(587-590 is good): ",c.status_cd)

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

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)