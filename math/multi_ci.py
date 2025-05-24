import scipy.stats as stats
import numpy as np

n = 65000   #测试次数，对于经验公式而言是每行次数
alpha = 0.05    # 1-alpha 代表置信水平
wi = np.array([75,75,75,75,75]) #每行补刀花费
x_real = 1 - np.array([0.9,0.84,0.96,0.57,0.39])
# 预设失败率真实值 = 1 - 预设成功率真实值
real = x_real.dot(wi)   #预设的补刀期望真实值

# 模拟进行测试
randmat = np.random.rand(n,x_real.size)
resmat = (randmat < x_real).astype(int)
xi :np.ndarray = np.mean(resmat, axis=0) #每行失败率测得值，用于经验公式
Xj :np.ndarray = resmat.dot(wi) #每次测试总补刀花费，用于全图估计

# 正态分布 上 alpha/2 分位数
quantile = stats.norm.ppf(1-alpha/2,loc=0,scale=1)

#全图测试估计
X_bar = Xj.mean()
width = np.std(Xj, ddof=1) * quantile / np.sqrt(n)
inf = X_bar - width
sup = X_bar + width

#经验公式估计
xbar_sum = xi.dot(wi)
width2 = np.sqrt( np.power(wi,2).dot(xi*(1-xi)) / (n) ) * quantile
inf2 = xbar_sum - width2
sup2 = xbar_sum + width2

print(f"预设真实值 {real:.2f}")
print(f"全图测试区间估计 ( {inf:.4f}, {sup:.4f} )")
print(f"经验公式估计 ( {inf2:.4f}, {sup2:.4f} )")
