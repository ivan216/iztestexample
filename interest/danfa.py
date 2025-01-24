from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        -1 -1
        3-4
        .....
        .....
        ...t1
        .....
        .....
        xg
        0  
        3-6 ''')
    
    test_count = 100

    @iz_test.check_tests_end()
    def end_test_callback(n, ns):
        nonlocal test_count
        if n < test_count:
            return None #注意是none，false是直接结束进程
        return ns/n

    iz_test.start_test(jump_frame=1, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)