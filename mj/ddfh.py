from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.iztest.dancing import get_dancing_manipulator

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0 3-0 5-0
        .s...
        .....
        bzp3w
        d__ts
        ppppz
        lz 
        0  
        4-6''')
    
    three_fail = 0
    four_fail = 0
    five_fail = 0

    dm = get_dancing_manipulator(iz_test)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        pl = iz_test.ground["4-5"]
        await until(lambda _:pl.hp <= 140)
        mj = place("mj 4-8")
        
        dm.start("move")

        # while True:
        #     await delay(27)
        #     if mj.x < 76:
        #         break
        #     dm.next_phase("d")
        #     await delay(1)
        #     dm.next_phase("m")
            
        await dm.until_next_phase("summon",lambda _:mj.x < 76)
        await delay(192) # 不发愣
        dm.next_phase("move")

    @iz_test.on_game_end()
    def _(result: bool):
        nonlocal three_fail,four_fail,five_fail
        if not result: 
            if iz_test.ground["3-0"] is not None:
                three_fail += 1
            if iz_test.ground["4-0"] is not None:
                four_fail += 1
            if iz_test.ground["5-0"] is not None:
                five_fail += 1

    iz_test.start_test(jump_frame=0, speed_rate=2)
    print("三路失败：",three_fail)
    print("四路失败：",four_fail)
    print("五路失败：",five_fail)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
