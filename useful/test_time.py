from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    n_succ = 1000  #测试至 达到此成功次数才停止

    iz_test = IzTest(ctler).init_by_str('''
        -1 -1
        3-0
        .....
        .....
        psso.
        .....
        .....
        cg
        0
        3-6''')
    
    succ_time_sum = 0
    game_res = False

    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal game_res
        game_res = res

    @iz_test.flow_factory.add_destructor()
    def _(fm):
        nonlocal succ_time_sum, game_res
        if game_res:
            succ_time_sum += fm.time - 2  # 减去2cs才是真正用时

    @iz_test.check_tests_end()
    def _(n,ns):
        nonlocal n_succ
        if ns < n_succ and n < 100000: #超10万次强制结束
            return None
        return ns/n

    iz_test.start_test(jump_frame=1, print_interval=100)

    aver_succ = succ_time_sum / iz_test._success_count if iz_test._success_count != 0 else -1
    print(f"测试{iz_test._test_time}次, 成功{iz_test._success_count}次, 成功平均用时{aver_succ:.2f}cs")

with InjectedGame(game_path) as game:
    fun(game.controller)
