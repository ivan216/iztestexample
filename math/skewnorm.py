from scipy.optimize import fsolve
import numpy as np
from scipy.stats import skewnorm


def fit_skewnormal(mean, variance, skewness):
    """根据均值、方差和偏度拟合偏正态分布参数"""
    # 1. 从偏度求解δ
    c = 2/np.pi
    k = (4 - np.pi)/2 * np.power(c,3/2)
    
    def eq_delta(delta):
        return k * delta**3 / (1 - c*delta**2)**1.5 - skewness
    
    delta0 = 0.8 if skewness > 0 else -0.8
    delta = fsolve(eq_delta, delta0)[0]
    delta = np.clip(delta, -0.999, 0.999)
    
    # 2. 计算α
    alpha = delta / np.sqrt(1 - delta**2)
    
    # 3. 计算ω
    omega = np.sqrt(variance / (1 - 2*delta**2/np.pi))
    
    # 4. 计算ξ
    xi = mean - omega * delta * np.sqrt(2/np.pi)
    
    return xi, omega, alpha

# 示例验证 =====================================
# 设定目标参数
target_mean = 5.0
target_variance = 4.0
target_skewness = 0.7

# 拟合参数
xi, omega, alpha = fit_skewnormal(target_mean, target_variance, target_skewness)

# 生成分布验证
dist = skewnorm(alpha, loc=xi, scale=omega)
samples = dist.rvs(size=100000)

# 计算样本统计量
calc_mean = np.mean(samples)
calc_var = np.var(samples)
calc_skew = np.mean((samples - calc_mean)**3) / calc_var**1.5

print(f"目标统计量: 均值={target_mean:.2f}, 方差={target_variance:.2f}, 偏度={target_skewness:.2f}")
print(f"拟合参数: ξ={xi:.3f}, ω={omega:.3f}, α={alpha:.3f}")
print(f"样本统计量: 均值={calc_mean:.3f}, 方差={calc_var:.3f}, 偏度={calc_skew:.3f}")
