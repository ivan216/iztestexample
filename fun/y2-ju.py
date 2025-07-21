from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler:Controller):
    n = 2000
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        1-0 2-0 3-0 4-0 5-0
        yy...
        yy...
        yy...
        yy...
        yy...
        xg
        0  
        1-6 ''')
    
    zbx = (9-1)*80 + 10.0
    succ_cnt = 0

    @iz_test.flow_factory.add_flow()
    async def _(_):
        zb = iz_test.ground.zombie(0)
        zb.die_no_loot()

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        zb = iz_test.game_board.iz_place_zombie(0,8,ZombieType.gargantuar)
        zb.x = zbx
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        zb = iz_test.game_board.iz_place_zombie(1,8,ZombieType.gargantuar)
        zb.x = zbx

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        zb = iz_test.game_board.iz_place_zombie(2,8,ZombieType.gargantuar)
        zb.x = zbx

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        zb = iz_test.game_board.iz_place_zombie(3,8,ZombieType.gargantuar)
        zb.x = zbx

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        zb = iz_test.game_board.iz_place_zombie(4,8,ZombieType.gargantuar)
        zb.x = zbx
    
    @iz_test.on_game_end()
    def _(_):
        nonlocal succ_cnt
        if iz_test.ground['1-0'] is not None:
            succ_cnt += 1
        if iz_test.ground['2-0'] is not None:
            succ_cnt += 1
        if iz_test.ground['3-0'] is not None:
            succ_cnt += 1
        if iz_test.ground['4-0'] is not None:
            succ_cnt += 1
        if iz_test.ground['5-0'] is not None:
            succ_cnt += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=1, print_interval=100)
    print(n * 5)
    print(succ_cnt)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)