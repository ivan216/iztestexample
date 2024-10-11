from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        500 -1
        3-0
        .....
        .....
        pblh2
        .....
        .....
        tt lz
        0  20
        3-6 3-6                       
        ''') #
    # lz(0) tt(1) 81-83%
    # lz(1) tt(0) 77-81%
    # tt(0) lz(1) 83%
    # tt(1) lz(0) 83-85%

    xg_count = 0
    zb_x = 0
    p_hp = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal xg_count,zb_x,p_hp
        p = iz_test.ground["3-1"]
        tt = iz_test.ground.zombie(0)
        await delay(20)
        lz = iz_test.ground.zombie(1)

        setx = 110
        sethp = 200
        
        await (until(lambda _:lz.hp < 90) | until(lambda _:tt.hp < 90))
        if lz.hp < 90:
            await until(lambda _:tt.hp < sethp)
            if tt.x > setx:
                place("xg 3-6")
                xg_count += 1
        else:
            await until(lambda _:lz.hp < sethp)
            if lz.x > setx:
                place("xg 3-6")
                xg_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
