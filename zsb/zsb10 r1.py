from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller

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
        zlist = iz_test.game_board.zombie_list
        tt = zlist[0]        
        plist = iz_test.ground
        h = plist["1-5"]
        c = plist["2-3"]
        y = plist["1-1"]
        
        await (until(lambda _:h.is_dead) | until(lambda _:tt.hp <90))
        if h.is_dead:
            await (until(lambda _:tt.hp <= 110) | until(lambda _:tt.int_x <= 330))
            cg = place("cg 1-6")
            cg_count += 1
        else:
            place("xg 1-6")
            xg_count += 1
            await until(lambda _:h.is_dead)
            cg = place("cg 1-6")
            cg_count += 1

        while not y.is_dead:
            await until(lambda _:cg.butter_cd > 0)   #过不去必定中了黄油，因此判断黄油就行
            if  cg.int_x > 63 :
                cg = place("cg 1-6")
                cg_count += 1
            await until(lambda _:cg.hp < 170)
            if len(list(~iz_test.game_board.zombie_list)) <=1:  #场上小于等于1个僵尸那么才需要补
                cg = place("cg 1-6")
                cg_count += 1
            else:
                await until(lambda _:len(list(~iz_test.game_board.zombie_list)) == 0)   #等到都死了，就要补杆
                cg = place("cg 1-6")
                cg_count += 1

        # while not y.is_dead:
        #     await until(lambda _:cg.hp <= 170)
        #     cg = place("cg 1-6")
        #     cg_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(cg_count)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)