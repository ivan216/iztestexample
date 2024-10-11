from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.iztest.cond_funcs import until_n_butter

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0
        y_p_h
        dpczh
        bs5tz
        13jlo
        ppwph
        tt 
        0  
        1-6 ''')
    
    cg_count =0
    xg_count =0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal cg_count,xg_count
        tt = iz_test.game_board.zombie_list[0]       
        plist = iz_test.ground
        h = plist["1-5"]
        c = plist["2-3"]
        y = plist["1-1"]
        
        await (until(lambda _:h.is_dead or tt.hp <90) | until_n_butter(y,2).after(142))
        if h.is_dead:
            await until(lambda _:tt.hp <= 110 or tt.int_x <= 330)
            cg = place("cg 1-6")
            cg_count += 1
        else:
            place("xg 1-6")
            xg_count += 1
            await until(lambda _:h.is_dead)
            cg = place("cg 1-6")
            cg_count += 1

        while not y.is_dead:
            await until(lambda _:cg.hp < 170)
            cg = place("cg 1-6")
            cg_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(cg_count)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)