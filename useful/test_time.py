from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    n = 1000
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        3-0
        .....
        .....
        psso.
        .....
        .....
        cg
        0
        3-6''')
    
    succ_time = 0
    game_res = False

    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal game_res
        game_res = res

    @iz_test.flow_factory.add_destructor()
    def _(fm:FlowManager):
        nonlocal succ_time, game_res
        if game_res:
            succ_time += fm.time - 1

    iz_test.start_test(jump_frame=1, print_interval=100)

    aver_succ = succ_time / iz_test._success_count if iz_test._success_count != 0 else -1
    print(f"测试{n}次, 成功{iz_test._success_count}次, 成功平均用时{aver_succ:.2f}cs")

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
