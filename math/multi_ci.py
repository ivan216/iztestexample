import random
import scipy.stats as stats
import numpy as np

n = 16000   #测试次数，对于经验公式而言是每行次数
alpha = 0.05    # 1-alpha 代表置信水平
wi = np.array([75,75,75,75,75]) #每行补刀花费
x_real = 1 - np.array([0.9,0.84,0.96,0.57,0.39])
# 1 - 预设成功率真实值 = 预设失败率真实值
Xj = np.zeros(n)    #每次测试总补刀花费，用于全图估计
xi = np.zeros(x_real.size) #每行失败率测得值，用于经验公式

real = sum(x_real*wi)   #预设的补刀期望真实值

# 模拟进行测试
for j in range(n):
    for i in range(x_real.size):
        rand = random.random()
        if rand < x_real[i]:    #失败
            Xj[j] += wi[i]  #记录补刀花费
            xi[i] += 1 #记录失败次数

quantile = stats.norm.ppf(1-alpha/2,loc=0,scale=1)

#全图测试估计
X_bar = Xj.mean()
sample_std = np.std(Xj, ddof=1)
width = sample_std * quantile / np.sqrt(n)
inf = X_bar - width
sup = X_bar + width

#经验公式估计
xi = xi / n   #每行测得失败率
sample_sum = sum(xi*wi)
width2 = np.sqrt( sum(wi**2 *xi*(1-xi))/(n) ) * quantile
inf2 = sample_sum - width2
sup2 = sample_sum + width2


print("预设真实值 %.2f"%real)
print("全图测试区间估计 ( %.4f"%inf,",%.4f"%sup,")")
print("经验公式估计 ( %.4f"%inf2,",%.4f"%sup2,")")
