import numpy as np

def fit_skewnormal(mean, variance, skewness)->tuple[float, float, float]:
    """
    根据均值 μ, 方差 σ², 偏度 γ, 拟合偏正态分布参数 位置 ξ, 尺度 ω, 形状 α

    f(x) = (2/ω) * φ((x-ξ)/ω) * Φ(α*(x-ξ)/ω)

    取 δ = α / √(1+α²) , c = 2/π , k = (4-π)/2 * √c³ , 则

    均值 μ = ξ + ω * δ * √c

    方差 σ² = ω² * (1 - c*δ²)

    偏度 γ = k * δ³ / √(1-c*δ²)³

    容易解出 δ² = ∛(γ/k)² / (1 + c * ∛(γ/k)²) , 代入并依次计算可得 α, ω, ξ
    """
    
    c = 2/np.pi
    # 1. 从偏度 γ 求解 δ
    k = (4 - np.pi)/2 * np.power(c,3/2)
    skew_div_k = np.power(np.abs(skewness)/k,2/3)
    delta = np.sign(skewness) * np.sqrt(skew_div_k / (1+c*skew_div_k))
    # 2. 计算 α
    alpha = delta / np.sqrt(1 - delta**2)
    # 3. 计算 ω
    omega = np.sqrt(variance / (1 - c*delta**2))
    # 4. 计算 ξ
    ksi = mean - omega * delta * np.sqrt(c)
    
    return ksi, omega, alpha

if __name__ == '__main__':
    from scipy.stats import skewnorm
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
    calc_var = np.var(samples,ddof=1)
    from scipy.stats import skew
    calc_skew = skew(samples)

    print(f"目标统计量: 均值={target_mean:.3f}, 方差={target_variance:.3f}, 偏度={target_skewness:.3f}")
    print(f"拟合参数: ξ={ksi:.3f}, ω={omega:.3f}, α={alpha:.3f}")
    print(f"样本统计量: 均值={calc_mean:.3f}, 方差={calc_var:.3f}, 偏度={calc_skew:.3f}")
