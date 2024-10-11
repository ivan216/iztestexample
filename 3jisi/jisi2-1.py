from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.dancing import partner

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0 2-0 3-0
        dwptz
        .ppts
        p__hw
        .....
        .....
        mj 
        0  
        2-9''')
    
    _1_fail = _2_fail = _3_fail = 0
    _50_count = 0
    both = 0
    print()

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        mj = iz_test.game_board.zombie_list[0]
        mjc = 242   #2-9 242 84%  #2-6 
        iz_test.game_board.mj_clock = randint(mjc,mjc+10)

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50_count,both
        t_die = False
        p = iz_test.ground["2-2"]
        t = iz_test.ground["2-4"]
        mj2 = iz_test.game_board.zombie_list[0]

        await until(lambda _:mj2.status is ZombieStatus.dancing_summoning)
        wb = partner(mj2,"a")
        await until(lambda _:wb.hp < 90)
        if not t.is_dead:
            await delay(25) #反应时间
            place("xg 2-6")
            _50_count += 1
            both += 1
        else:
            t_die = True
        
        for _ in range(2):      #一直到第二只前舞伴
            await until(lambda _:wb is None or wb.is_dead)
            while wb is None or wb.is_dead:
                await until(lambda _:mj2.status is ZombieStatus.dancing_summoning)
                wb = partner(mj2,"a")

        if t_die:
            await until(lambda _:wb.status != ZombieStatus.backup_spawning).after(4)
            if wb.x < 166:
                if not wb.is_eating :
                    place("xg 2-6")
                    _50_count += 1

        await until(lambda _:wb.hp < 90)
        place("xg 2-6")
        _50_count += 1

    @iz_test.on_game_end()
    def count(_):
        nonlocal _1_fail,_2_fail,_3_fail
        if iz_test.ground["1-0"] is not None:
            _1_fail += 1
        if iz_test.ground["2-0"] is not None:
            _2_fail += 1
        if iz_test.ground["3-0"] is not None:
            _3_fail += 1
    
    # @iz_test.flow_factory.add_tick_runner()
    # def show(_):
    #     mj = iz_test.game_board.zombie_list[0]
    #     print("\033[A\033[K",hex(mj.status))
    
    iz_test.start_test(jump_frame=1, speed_rate=10)
    print("1失败 ",_1_fail)
    print("2失败 ",_2_fail)
    print("3失败 ",_3_fail)
    print("补50 ",_50_count)
    print(both)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)