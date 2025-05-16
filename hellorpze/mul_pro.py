import multiprocessing
from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler, n):
    simu = 0  # 记录同归于尽次数
    prt_intvl = 100  # 屏幕输出间隔

    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        3-0
        .....
        .....
        yssss
        .....
        .....
        lz
        0  
        3-6 ''')

    @iz_test.on_game_end()
    def _(res):
        nonlocal simu
        if not res:
            if iz_test.ground['3-1'] is None:
                simu += 1
        if iz_test._test_time % prt_intvl == prt_intvl - 1 :
            print(f"pid {ctler.pid} :")  # 输出pid

    p, _ = iz_test.start_test(jump_frame=True, print_interval=prt_intvl)
    return p, simu  # 返回: 过率, 同归于尽次数


def testing(n):
    with InjectedGame(game_path) as game:
        return fun(game.controller, n)


if __name__ == "__main__":
    pros = 3   # 进程数，建议只取 2,3,4
    testnum = 1000  # 总次数

    numlist = [testnum//pros for _ in range(pros)]  # 表示每个进程测试次数的列表
    numlist[0] += (testnum % pros)  # 多余的次数补到第一个进程

    # 开始测试, 返回值存到output里面
    with multiprocessing.Pool(processes=pros) as pool:   
        output = pool.map(testing, numlist)

    # 计算总过率
    val1 = sum(x*y[0] for x,y in zip(numlist,output)) / testnum
    # 计算总同归于尽次数
    val2 = sum(x[1] for x in output)

    print()
    print(f"总过率 {val1:.2%}")
    print(f"总同归于尽次数 {val2}")
