from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus,Zombie
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun
from rpze.iztest.dancing import partner
from random import randint

# 约 1110

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        
        bppch                                
        blpsh
        3y_h_
        .....
        .....
        cg   lz    lz   mj
        0    180   200  220
        2-6  2-6   2-6  2-6  ''')
    
    cg_count = tt_count = ft_count =  xt1_count = _25_count = 0
    xt_count = xg_count = tt2_count = lz2_count = cg2_count = 0             #计数值初始化
    tp_fail = _1_fail = _2_fail = _3_fail = 0
    lz1 = lz2 = mj = wbw = wbs = None                                       #僵尸
    b = tp = p2 = p3 = c = y = h1 = h3 = None                               #植物
    nao1 = nao2 = nao3 = None
    bu1 = bu3 = can_end = bu_tou = False                                    #启用结束判断 标志
    # h1_record = [0 for _ in range(9)]
    # h3_record = [0 for _ in range(9)]

    @iz_test.flow_factory.add_flow()    #专门开一个add_flow 存植物与僵尸，方便其他add_flow调用
    async def _(_):
        nonlocal lz1,lz2,mj
        nonlocal b,tp,p2,p3,c,y,h1,h3
        nonlocal nao1,nao2,nao3
        
        nao1 = iz_test.ground["1-0"]
        nao2 = iz_test.ground["2-0"]
        nao3 = iz_test.ground["3-0"]
        p2 = iz_test.ground["1-2"]
        p3 = iz_test.ground["1-3"]
        c = iz_test.ground["1-4"]
        b = iz_test.ground["2-1"]
        tp = iz_test.ground["3-1"]
        y = iz_test.ground["3-2"]
        h1 = iz_test.ground["1-5"]
        h3 = iz_test.ground["3-4"]

        await delay(180)
        lz1=iz_test.game_board.zombie_list[1]
        await delay(20)
        lz2=iz_test.game_board.zombie_list[2]
        await delay(20)
        mj=iz_test.game_board.zombie_list[3]


    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal xt_count,bu_tou
        await delay(220)
        await until(lambda _:lz1.hp<90 and lz2.hp<90 or nao2.is_dead)
        wb1:Zombie = partner(mj,"a")
        await until(lambda _:wb1 is None or wb1.hp<90 or b.is_dead)
        
        if not b.is_dead:
            if not bu_tou:
                place("xt 3-1")
                xt_count += 1
                bu_tou = True


    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal xt_count,bu_tou
        await delay(220)
        
        while not tp.is_dead:
            await until (lambda _:mj.status==ZombieStatus.dancing_summoning)
            wbw2:Zombie = partner(mj,"w")
            wbs2:Zombie = partner(mj,"s")

            if wbw2 is not None and wbs2 is not None:
                if wbw2.status is ZombieStatus.backup_spawning and wbs2.status is ZombieStatus.backup_spawning:
                    await delay(170)
                    if 80<mj.int_x<100 and mj.hp<500 and (wbw2.is_eating or wbs2.is_eating):
                        if not bu_tou:
                            place("xt 3-1")
                            xt_count += 1
                            bu_tou = True
                            await until(lambda _:tp.is_dead)


    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal xg_count
        await delay(220)
        await until(lambda _:mj.int_x<240) 
        wb:Zombie = partner(mj,"s")
        i = get_sunflower_remaining_sun(h3)
        if i > 25:
            await until(lambda _:wb is None or wb.is_dead)
            await until(lambda _:mj.status==ZombieStatus.dancing_summoning).after(220)
            place("xg 3-6")
            xg_count += 1
            h3.die()    #当作全部成功补

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal can_end,bu1,bu3,bu_tou
        nonlocal wbs,wbw

        can_end = bu1 = bu3 = bu_tou = False              # 每次新测试记得先把标志设置成false
        await delay(220)
        
        await (until(lambda _:mj.hp < 170)      #mj掉头
               |until(lambda _:nao1.is_dead and nao2.is_dead and nao3.is_dead))
        if nao1.is_dead and nao2.is_dead and nao3.is_dead :     #脑子全被吃完，直接判赢
            return iz_test.end(True)
        
        wbw:Zombie = partner(mj,"w")
        wbs:Zombie = partner(mj,"s")
        bu1 = True
        bu3 = True
        
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal bu1,can_end,wbw
        nonlocal cg_count,tt_count,ft_count,xt1_count

        await until(lambda _:bu1 is True)
        await (until(lambda _:wbw is None or wbw.hp < 90) | until(lambda _:nao1.is_dead))

        if not nao1.is_dead:
            if c.is_dead:
                if p3.is_dead:
                    place("cg 1-6")
                    cg_count += 1
                elif p2.is_dead:
                    place("tt 1-6")
                    tt_count += 1
                else:
                    place("ft 1-6")
                    ft_count += 1
            elif not p2.is_dead and not p3.is_dead:
                place("xt 1-1")
                xt1_count += 1
                await delay(400)
                place("cg 1-6")
                cg_count += 1
            else:
                place("cg 1-6")
                await delay(400)
                place("lz 1-6")
                cg_count += 2

        can_end = True      #补刀也全部写好了，可以启用结束检查
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal bu3,can_end,wbs,cg2_count,tt2_count,lz2_count,_25_count

        await until(lambda _:bu3 is True)
        await (until(lambda _:wbs is None or wbs.hp < 90)| until(lambda _:nao3.is_dead))

        if not nao3.is_dead:
            if h3.is_dead:
                place("cg 3-6")
                cg2_count += 1
            elif not y.is_dead:
                place("tt 3-6")
                tt2_count += 1
            else:
                place("lz 3-6")
                lz2_count += 1
        else:
            if not h3.is_dead:
                _25_count += 1

        can_end = True      #补刀也全部写好了，可以启用结束检查

    @iz_test.flow_factory.add_tick_runner()
    def _(_):
        if can_end:     #检查被启用后
            if iz_test.ground["3-0"] is None and iz_test.ground["1-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0: #僵尸全没了
                return iz_test.end(False)
    
    @iz_test.on_game_end()
    def _(_):
        nonlocal _1_fail,_2_fail,_3_fail,tp_fail

        # if h1 is None:
        #     i = 0
        # else:
        #     i = get_sunflower_remaining_sun(h1) // 25
        # h1_record[i] += 1 
        # if h3 is None:
        #     i = 0
        # else:
        #     i = get_sunflower_remaining_sun(h3) // 25
        # h3_record[i] += 1

        if not nao1.is_dead :
            _1_fail += 1
        if not nao2.is_dead :
            _2_fail += 1
        if not nao3.is_dead :
            _3_fail += 1
        if not tp.is_dead:
            tp_fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=10)
    print("1路补75：",cg_count)
    print("1路补桶 ",tt_count)
    print("1路补梯 ",ft_count)
    print("1路补偷 ",xt1_count)
    print()
    print("3路补偷 ",xt_count)
    print("3路补鬼 ",xg_count)
    print("3路补桶 ",tt2_count)
    print("3路补障 ",lz2_count)
    print("3路补杆 ",cg2_count)
    print()
    print("漏三线 ",tp_fail)
    print("漏25：",_25_count)
    print("1脑未收 ",_1_fail)
    print("2脑未收 ",_2_fail)
    print("3脑未收 ",_3_fail)

    # print("h1漏花情况 ",h1_record)
    # print("h3漏花情况 ",h3_record)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    