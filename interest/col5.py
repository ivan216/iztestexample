from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        ....d
        .....
        .....
        xg
        0  
        3-6 ''')
    
    pl = None
    next_frame = False
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal pl ,next_frame
        next_frame = False

        pl = iz_test.ground["3-5"]
        pl.generate_cd = 71

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        nonlocal next_frame
        if fm.time > 0 :
            if next_frame :
                pl.generate_cd = 136
                next_frame = False
            if pl.generate_cd == 1:
                next_frame = True

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        zb = iz_test.game_board.zombie_list[0]
        if fm.time > 0:
            print("time: ",fm.time," pl.hp ",pl.hp," zb.hp: ",zb.hp," gcd: ",pl.generate_cd," lcd: ",pl.launch_cd)

    iz_test.start_test(jump_frame=0, speed_rate=0.2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
