from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.iztest.cond_funcs import until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 4-0 5-0
        y_p_h
        dpczh
        bs5tz
        13jlo
        ppwph
        tt 
        0  
        1-6 ''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        plist = iz_test.ground
        c = plist["2-3"]
        star = plist["3-3"]
        await until(lambda _:c.status_cd >0).after(30)
        kg = place("kg 4-6")
        await delay(20)
        place("kg 2-6")
        await delay(20)
        place("cg 4-6")
        await until(lambda _:kg.int_x < 40)
        await until(lambda _:kg.int_x >= 260)
        await until_plant_n_shoot(star).after(60)
        place("mj 4-6")

    iz_test.start_test(jump_frame=0, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)