from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.plant import PlantStatus
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.cond_funcs import until_plant_n_shoot
from random import randint
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        wdtss
        .....
        .....
        .....
        lz 
        0  
        2-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["2-2"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:lz.x < 311)
        await until_plant_n_shoot(d).after(48 + randint(0,10))
        place("xg 2-6")

    @iz_test.flow_factory.add_tick_runner()
    def _(_):
        if iz_test.game_board.zombie_list.obj_num == 0:
            w = iz_test.ground["2-1"]
            if w.status is PlantStatus.squash_jump_down:
                return iz_test.end(True)
            else:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=10)

with InjectedGame(game_path) as game:
    fun(game.controller)