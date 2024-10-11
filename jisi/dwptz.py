from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.structs.plant import PlantStatus
from rpze.iztest.cond_funcs import until_plant_n_shoot

# 补21%杆

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        3-0
        .....
        .....
        dwpts
        .....
        .....
        lz 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        d = iz_test.ground["3-1"]
        w = iz_test.ground["3-2"]
        p = iz_test.ground["3-3"]
        z = iz_test.ground["3-5"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:z.hp < 20) #20
        await until_plant_n_shoot(d).after(40 + randint(0,10)) #40
        place("xg 3-6")

        await until(lambda _:w.status is PlantStatus.squash_look)
        return iz_test.end(True)

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)