from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place , repeat
from rpze.flow.utils import until ,delay
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.flow.flow import FlowManager
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        zdtoz
        .....
        .....
        .....
        .....
        xg 
        0  
        1-7''')

    time_begin = 0
    time_now = 0
    dz_eat = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal dz_eat
        plist = iz_test.ground
        d = plist["1-2"]
        z = plist["1-5"]
        z2 = plist["1-1"]

        await until_plant_last_shoot(d)
        await repeat("lz 1-6")
        await until(lambda _:z.hp < 12)
        place("cg 1-6")
        await until(lambda _: z2.status_cd >0)
        dz_eat += 1

    @iz_test.flow_factory.add_tick_runner()
    def time_rec(fm :FlowManager):
        nonlocal time_begin,time_now
        if time_begin == 0:
            time_begin = fm.time
        time_now = fm.time

    @iz_test.flow_factory.add_tick_runner()
    def check_end(_):
        nonlocal time_begin,time_now
        if iz_test.game_board.griditem_list[0].id.rank == 0 :
            return iz_test.end(True)
        if time_now - time_begin > 6000 :
            return iz_test.end(False)

    iz_test.start_test(jump_frame=0, speed_rate=10)
    print(dz_eat)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
