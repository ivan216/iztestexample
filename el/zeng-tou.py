from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.structs.zombie import ZombieStatus
from rpze.structs.plant import PlantType
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-2
        .....
        .....
        .o...
        .....
        .....
        xt 
        0  
        3-2''')
    
    zb = None
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal zb
        zb = iz_test.game_board.zombie_list[0]
        yy = iz_test.game_board.new_plant(1,0,PlantType.gloomshroom)
        yy2 = iz_test.game_board.new_plant(1,1,PlantType.gloomshroom)
        yy3 = iz_test.game_board.new_plant(1,2,PlantType.gloomshroom)
        yy4 = iz_test.game_board.new_plant(3,0,PlantType.gloomshroom)
        yy5 = iz_test.game_board.new_plant(3,1,PlantType.gloomshroom)
        yy6 = iz_test.game_board.new_plant(3,2,PlantType.gloomshroom)

        await until(lambda _:zb.status is ZombieStatus.bungee_idle_after_drop)
        yy.generate_cd = yy2.generate_cd = yy3.generate_cd \
        = yy4.generate_cd = yy5.generate_cd = yy6.generate_cd = 200
    
    iz_test.start_test(jump_frame=1, speed_rate=2,print_interval=5e2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
