import numpy as np
from scipy.stats import gamma
import matplotlib.pyplot as plt

def fit_gamma(mean, variance, skewness)->tuple[float, float, float]:
    if skewness <= 0 :
        raise ValueError("skewness must be positive")
    
    alpha = 4 / skewness**2
    beta = np.sqrt(alpha / variance)
    c = mean - alpha / beta

    return alpha, beta, c

if __name__ == "__main__":
    mean = 5
    variance = 2
    skewness = 1

    alpha, beta, c = fit_gamma(mean, variance, skewness)

    dist = gamma(alpha, loc = c, scale = 1/beta)
    samples = dist.rvs(size=100000)
    calc_mean = np.mean(samples)
    calc_var = np.var(samples,ddof=1)
    from scipy.stats import skew
    calc_skew = skew(samples)


    print(f"目标统计量: 均值={mean:.3f}, 方差={variance:.3f}, 偏度={skewness:.3f}")
    print(f"拟合参数: α={alpha:.3f}, β={beta:.3f}, c={c:.3f}")
    print(f"计算统计量: 均值={calc_mean:.3f}, 方差={calc_var:.3f}, 偏度={calc_skew:.3f}")
