from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.zombie import ZombieStatus

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0
        .....
        t....
        ...c.
        bl...
        .....
        kg  kg
        0   915
        2-6 4-6''')
    

    @iz_test.flow_factory.add_tick_runner()
    def print_no_pause_time(fm:FlowManager):
        c = iz_test.ground["3-4"]
        if fm.time > 1401:
            kg = iz_test.game_board.zombie_list[1]
            if kg.status == ZombieStatus.digger_lost_dig :
                print("lost dig: ",fm.time)
        print("time: ",fm.time," mag_cd: ",c.status_cd)
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)