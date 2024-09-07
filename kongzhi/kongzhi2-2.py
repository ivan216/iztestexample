from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun
from rpze.iztest.dancing import partner
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        bppch                                
        blpsh
        3y_h_
        byy_l
        .....
        cg   lz    lz   mj
        0    180   200  220
        2-6  2-6   2-6  2-6  ''')
    
    xt_count = cg_count = tt_count = ft_count = lousan = xt2_count = 0  #计数值初始化
    lz1 = lz2 = mj = None                                               #僵尸
    b = tp = p1 = p2 = c = y = nao1 = nao2 = nao3 = None                #植物
    can_end = False                                                     #启用结束判断 标志


    @iz_test.flow_factory.add_flow()    #专门开一个add_flow 存植物与僵尸，方便其他add_flow调用
    async def place_zombie(_):
        nonlocal lz1,lz2,mj
        nonlocal b,tp,p1,p2,c,y,nao1,nao2,nao3
        
        nao1 = iz_test.ground["1-0"]
        nao2 = iz_test.ground["2-0"]
        nao3 = iz_test.ground["3-0"]
        p1 = iz_test.ground["1-2"]
        p2 = iz_test.ground["1-3"]
        c = iz_test.ground["1-4"]
        b = iz_test.ground["2-1"]
        tp = iz_test.ground["3-1"]
        y = iz_test.ground["3-2"]

        await delay(180)
        lz1=iz_test.game_board.zombie_list[1]
        await delay(20)
        lz2=iz_test.game_board.zombie_list[2]
        await delay(20)
        mj=iz_test.game_board.zombie_list[3]


    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal xt_count
        await delay(220)
        await until(lambda _:((lz1.hp<90) and (lz2.hp<90)) or nao2.is_dead)
        wb1 = partner(mj,"a")
        await until(lambda _:(wb1 is None) or (wb1.hp<90) or b.is_dead)
        
        if not b.is_dead:
            place("xt 3-1")
            xt_count += 1


    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal xt_count
        await delay(220)
        mj=iz_test.game_board.zombie_list[3]  #不加这句舞伴的智能提示出不来，不过不影响执行
        
        while not tp.is_dead:
            await until (lambda _:mj.status==ZombieStatus.dancing_summoning)
            wbs2 = partner(mj,"w")
            wbx2 = partner(mj,"s")

            if (wbs2 is not None) and (wbx2 is not None):
                if (wbs2.status is ZombieStatus.backup_spawning) and (wbx2.status is ZombieStatus.backup_spawning):
                    await delay(170)
                    if (80<mj.int_x<120) and (mj.hp<500) and ((wbs2.is_eating)or(wbx2.is_eating)):
                        place("xt 3-1")
                        xt_count += 1


    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal cg_count,tt_count,ft_count,lousan,xt2_count,can_end
        can_end= False                              # 每次新测试记得先把标志设置成false
        
        await (until(lambda _:iz_test.game_board.zombie_list.obj_num == 0)  #场上僵尸全部没了
               | until(lambda _:nao1.is_dead and nao2.is_dead and nao3.is_dead))    #脑子全被吃完了
        if nao1.is_dead and nao2.is_dead and nao3.is_dead :     #脑子全被吃完，直接判赢
            return iz_test.end(True)
                                    #否则就是僵尸全没了，开始执行下面
        if not nao1.is_dead :
            if c.is_dead:
                if p1.is_dead:
                    place("cg 1-6")
                    cg_count += 1
                elif p2.is_dead:
                    place("tt 1-6")
                    tt_count += 1
                else:
                    place("ft 1-6")
                    ft_count += 1
            elif (not p1.is_dead) and (not p2.is_dead):
                place("xt 1-1")
                xt2_count += 1
                await delay(400)
                place("cg 1-6")
                cg_count += 1
            else:
                place("cg 1-6")
                await delay(400)
                place("lz 1-6")
                cg_count += 2

        if not nao3.is_dead:
            place("cg 3-6")
            cg_count += 1
        if not tp.is_dead:
            lousan += 1
        
        can_end = True      #补刀也全部写好了，可以启用结束检查


    @iz_test.flow_factory.add_tick_runner()
    def check_end(_):
        if can_end:     #检查被启用后
            if iz_test.ground["3-0"] is None and iz_test.ground["1-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0: #僵尸全没了
                return iz_test.end(False)
            

    iz_test.start_test(jump_frame=1, speed_rate=10)
    print("3路补偷",xt_count)
    print("补75数",cg_count)
    print("补125数",tt_count)
    print("补150数",ft_count)
    print("漏三线",lousan)
    print("1路补偷",xt2_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)