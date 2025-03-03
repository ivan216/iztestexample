from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until, delay
from rpze.rp_extend import Controller
from random import randint

#算作270，不优

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        byy_l
        .....
        .....
        lz  gl 
        20  0
        3-6 3-6''')
    
    _75_count = 0

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count
        y = iz_test.ground["3-3"]
        b = iz_test.ground["3-1"]
        gl = iz_test.ground.zombie(0)   #释放顺序而非书写顺序
        await delay(20)
        lz = iz_test.ground.zombie(1)
        
        await until(lambda _:lz.hp < 90)  # 几乎没有橄榄先死的可能性，因此只关心路障。
        await until(lambda _:gl.accessories_hp_1 < 400)
        if gl.int_x > 200 : #还没碰到玉米
            await (until(lambda _:y.is_dead) | until(lambda _:gl.hp < 90))
            if y.is_dead :
                place("cg 3-6")
                _75_count += 1
            else:
                await repeat("cg 3-6")
                _75_count += 2
        else:
            await until(lambda _:gl.accessories_hp_1 < 100) 
            if not y.is_dead:
                await (until(lambda _:y.is_dead) | until(lambda _:gl.hp <90))
                if not y.is_dead:
                    await repeat("cg 3-6")
                    _75_count += 2
                else:
                    place("cg 3-6")
                    _75_count += 1   
            elif gl.int_x > 120: #没碰到2列玉米
                place("cg 3-6")
                _75_count += 1
            else:
                await (until(lambda _:b.is_dead) | until(lambda _:gl.hp <90))
                if not b.is_dead:
                    place("cg 3-6")
                    _75_count += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=10)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)