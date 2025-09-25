from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from msvcrt import getwch
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler: Controller):
    iz_test = IzTest(game.controller).init_by_str('''
        100 -1
        3-0
        .....
        .....
        1ssss
        .....
        .....
        lz
        0  
        3-6 ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        lz = iz_test.game_board.zombie_list[0]
        await until(lambda _: not lz.is_not_dying)

        ctler.end_jump_frame()
        # frame_duration 大于100可以逐帧播放,原因不明
        # frame_duration 大于200游戏会卡死
        iz_test.game_board.frame_duration = 101  

        print(f"paused, current tests: {iz_test._test_time + 1}")
        while iz_test.check_end() is None:  # 终止方法:狂按 ctrl+C
            gc = getwch()
            if gc == 'w':
                ctler.skip_frames()
            elif gc == 'q':
                ctler.skip_frames(100)
            else:
                break
        ctler.start_jump_frame()
    
    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(game_path) as game:
    fun(game.controller)