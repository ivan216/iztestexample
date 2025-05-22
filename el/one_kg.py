# 单矿工伤害测试程序
from random import randint
import numpy as np
import matplotlib.pyplot as plt

a = 1
n = 6
test_N = a * 10**n  # 测试次数

num_act = 0
num_not_act = 4  # 静曾

plant_list = [True]*num_act+[False]*num_not_act

M_sup = 1001  #时间长度,不会超过1001cs
max_hp = 600  #不会超过600hp

class IO:
    def __init__(self,act):
        self.list = self.hit_list(act,[158,130,102,74],200,20)  # 74是第一次命中
    @staticmethod
    def hit_list(act, hits, max_cd, dmg):
        tmp = np.zeros(M_sup)  # 存储具体时间点的伤害

        # last_att 上一次判定到当前时刻过了多久
        # t 当前时间距离下一次判定的时长
        prob = randint(0,(max_cd-7)*15-1)    # 0-2894
        if prob < 15*(max_cd-14):
            t = 1 + prob//15  # 1-186
            last_att = randint(max_cd-14,max_cd) - t  
        else:
            t_list = [14,27,39,50,60,69,77,84,90,95,99,102,104,105]
            prob -= 15*(max_cd-14)    #[0,105)
            for i in range(14):
                if prob < t_list[i]:
                    t = max_cd -14 +i+1  # 187-200
                    last_att = randint(t, max_cd) - t
                    break

        if act:  # 动曾
            for hit in hits:
                if last_att < hit:    # -att__0__-att+74__...__-att+158，需要严格小于
                    tmp[hit-last_att] = dmg
        while True:
            intvl = randint(max_cd-14,max_cd)
            if t+intvl >= M_sup:  
                break
            for hit in hits:
                tmp[t+hit] = dmg  # 相应命中时间赋值
            t += intvl  # 更新下一个t
            
        return tmp

def test_dmg():
    plt :list[IO] = []
    for p in plant_list:  # 生成植物
        plt.append(IO(p))  # 每个植物都有对应时间点伤害

    hp = 300  # 15豌豆
    t_eat = randint(350,353)
    ans = 0

    for i in range(M_sup):
        for p in plt:
            if p.list[i] != 0:
                hp -= p.list[i]
        if hp <= 0:
            return ans
        if i >= t_eat and (i-t_eat) % 4 == 0: #啃食最后结算
            ans += 4
    print('excel')

def my_tst(N):
    num = max_hp//4
    ans = np.zeros(num)
    tmp = 1
    for i in range(N):
        res = test_dmg()
        ans[res//4] += 1
        if i+1 == round(N*(tmp/100)) :
            ht_count = np.dot(ans[1:], np.ones(num-1))
            ht_hp = np.dot(ans, np.array(range(num))*4)
            print(f"process:{100*(i+1)/N:.0f}%  hp:{ht_hp/(i+1):.5f}  count:{100*ht_count/(i+1):.3f}%")
            tmp += 1

    ht_count = np.dot(ans[1:], np.ones(num-1))
    ht_hp = np.dot(ans, np.array(range(num))*4)
    print(f"mean dmg:{ht_hp/N:.5f}  mean count:{100*ht_count/N:.3f}%")
    
    # 作图
    max_idx = np.nonzero(ans)[0][-1]
    x = np.array(range(max_idx+1)) * 4
    plt.bar(x,ans[0:max_idx+1])
    plt.yscale('log')
    plt.title(f"mean dmg:{ht_hp/N:.5f} dmg prob:{100*ht_count/N:.3f}%")
    plt.xlabel('dmg')
    plt.ylabel('frequency')
    plt.show()

my_tst(test_N)