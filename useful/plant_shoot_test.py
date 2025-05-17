from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.iztest.cond_funcs import until_plant_n_shoot
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        dbl5o
        .....
        .....
        .....
        tz 
        0  
        2-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["2-1"]
        await until_plant_n_shoot(d,2).after(30)
        place("tz 2-6")

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(game_path) as game:
    fun(game.controller)
    