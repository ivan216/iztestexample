from scipy.optimize import fsolve
import numpy as np
from scipy.stats import skewnorm

def fit_skewnormal(mean, variance, skewness)->tuple[float, float, float]:
    """
    根据均值 μ, 方差 σ², 偏度 γ, 拟合偏正态分布参数 ξ, ω, α

    f(x) = (2/ω) * φ((x-ξ)/ω) * Φ(α*(x-ξ)/ω)

    取 δ = α / √(1+α²) 则

    均值 μ = ξ + ω * δ * √(2/π)

    方差 σ² = ω² * (1 - 2*δ²/π)

    偏度 γ = (4-π)/2 * (δ*√(2/π))³ / (1-2*δ²/π)^1.5

    """
    # 1. 从偏度 γ 求解 δ
    c = 2/np.pi
    k = (4 - np.pi)/2 * np.power(c,3/2)
    
    def eq_delta(delta):
        return k * delta**3 / (1 - c*delta**2)**1.5 - skewness
    
    delta0 = 0.8 if skewness > 0 else -0.8
    delta = fsolve(eq_delta, delta0)[0]
    delta = np.clip(delta, -0.999, 0.999)
    
    # 2. 计算 α
    alpha = delta / np.sqrt(1 - delta**2)
    
    # 3. 计算 ω
    omega = np.sqrt(variance / (1 - c*delta**2))
    
    # 4. 计算 ξ
    ksi = mean - omega * delta * np.sqrt(c)
    
    return ksi, omega, alpha

if __name__ == '__main__':
# 示例验证 =====================================
# 设定目标参数
    target_mean = 5.0
    target_variance = 4.0
    target_skewness = 0.7

    # 拟合参数
    ksi, omega, alpha = fit_skewnormal(target_mean, target_variance, target_skewness)

    # 生成分布验证
    dist = skewnorm(alpha, loc=ksi, scale=omega)
    samples = dist.rvs(size=100000)

    # 计算样本统计量
    calc_mean = np.mean(samples)
    calc_var = np.var(samples)
    calc_skew = np.mean((samples - calc_mean)**3) / calc_var**1.5

    print(f"目标统计量: 均值={target_mean:.2f}, 方差={target_variance:.2f}, 偏度={target_skewness:.2f}")
    print(f"拟合参数: ξ={ksi:.3f}, ω={omega:.3f}, α={alpha:.3f}")
    print(f"样本统计量: 均值={calc_mean:.3f}, 方差={calc_var:.3f}, 偏度={calc_skew:.3f}")
