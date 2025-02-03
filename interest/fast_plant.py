from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.plant import PlantType

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        .ssss
        1ssss
        .....
        tt lz
        0  0
        3-6 4-6''')
    
    pl = None
    next_frame = False
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal pl ,next_frame
        next_frame = False
        pl = iz_test.game_board.new_plant(2,0,PlantType.melonpult)
        pl.generate_cd = 2  #2最快反应
        print()
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        nonlocal next_frame
        if fm.time > 0 :
            if next_frame :
                # pl.generate_cd = 136
                pl.generate_cd = 1  #1最小间隔
                next_frame = False
            if pl.generate_cd == 1:
                next_frame = True

            if pl.launch_cd > 2:
                pl.launch_cd = 2    #2最小launchcd

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 0:
            print(f"\033[A\033[K{pl.launch_cd}")
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
