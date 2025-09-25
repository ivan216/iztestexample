import numpy as np
from scipy.special import gammaln
from scipy.stats import gengamma
from scipy.optimize import minimize

def generalized_gamma_moments(params, mu, sigma2, skew):
    """计算广义伽马分布的矩与目标矩的差异"""
    a, c, theta = params
    
    # 安全检查参数范围
    if a <= 0 or theta <= 0 or abs(c) < 1e-6:
        return np.inf
    
    try:
        # 计算比率 r_k = Γ(a + k/c) / Γ(a)
        def r(k):
            return np.exp(gammaln(a + k/c) - gammaln(a))
        
        r1 = r(1)
        r2 = r(2)
        r3 = r(3)
        
        # 计算分布矩
        mean = theta * r1
        variance = theta**2 * (r2 - r1**2)
        
        # 计算三阶中心矩
        mu3 = theta**3 * (r3 - 3*r1*r2 + 2*r1**3)
        skewness = mu3 / (variance**1.5)
        
        # 计算与目标矩的差异
        mean_diff = (mean - mu)**2
        var_diff = (variance - sigma2)**2
        skew_diff = (skewness - skew)**2
        
        return mean_diff + var_diff + skew_diff
    
    except (ValueError, FloatingPointError):
        return np.inf

def fit_generalized_gamma(mu, sigma2, skew, initial_guess=None):
    """拟合广义伽马分布参数"""
    # 设置初始猜测值
    if initial_guess is None:
        # 基于伽马分布初始化 (c=1)
        a_guess = mu**2 / sigma2
        theta_guess = sigma2 / mu
        initial_guess = [a_guess, 1.0, theta_guess]
    
    # 设置参数边界 (a>0, β>0, c≠0)
    bounds = [
        (1e-6, None),    # a > 0
        (-10, 10),       # c ∈ [-10, 10] 排除0
        (1e-6, None)     # β > 0
    ]
    
    # 优化拟合
    result = minimize(
        fun=generalized_gamma_moments,
        x0=initial_guess,
        args=(mu, sigma2, skew),
        bounds=bounds,
        method='L-BFGS-B',  # 支持边界约束的优化方法
        options={'maxiter': 1000, 'ftol': 1e-8}
    )
    
    if not result.success:
        # 尝试其他初始值
        alt_guesses = [
            [mu, 0.5, sigma2],  # 对数正态类型
            [1.0, 2.0, mu],      # 威布尔类型
            [2.0, -1.0, sigma2]  # 倒伽马类型
        ]
        for guess in alt_guesses:
            result = minimize(
                generalized_gamma_moments,
                x0=guess,
                args=(mu, sigma2, skew),
                bounds=bounds,
                method='L-BFGS-B'
            )
            if result.success:
                break
    
    if result.success:
        a_fit, c_fit, theta_fit = result.x
        return a_fit, c_fit, theta_fit
    else:
        raise RuntimeError("拟合失败: " + result.message)

def calculate_fitted_moments(a, c, theta):
    """计算拟合分布的矩"""
    def r(k):
        return np.exp(gammaln(a + k/c) - gammaln(a))
    
    r1 = r(1)
    r2 = r(2)
    r3 = r(3)
    
    mean = theta * r1
    variance = theta**2 * (r2 - r1**2)
    mu3 = theta**3 * (r3 - 3*r1*r2 + 2*r1**3)
    skewness = mu3 / (variance**1.5)
    
    return mean, variance, skewness

# 示例使用 =============================================
if __name__ == "__main__":
    # 输入已知矩 (根据你的数据)
    mu = 5      # 均值
    sigma2 = 2  # 方差
    skew = 1     # 偏度
    
    try:
        # 拟合参数
        a, c, theta = fit_generalized_gamma(mu, sigma2, skew)
        
        # 计算拟合分布的矩
        fit_mean, fit_var, fit_skew = calculate_fitted_moments(a, c, theta)
        
        dist = gengamma(a=a, c=c, scale = theta)
        samples = dist.rvs(size=100000)
        calc_mean = np.mean(samples)
        calc_var = np.var(samples,ddof=1)
        from scipy.stats import skew
        calc_skew = skew(samples)


        print(f"目标统计量: 均值={fit_mean:.3f}, 方差={fit_var:.3f}, 偏度={fit_skew:.3f}")
        print(f"拟合参数: α={a:.3f}, c={c:.3f}, β={theta:.3f}")
        print(f"计算统计量: 均值={calc_mean:.3f}, 方差={calc_var:.3f}, 偏度={calc_skew:.3f}")
        
        # 检查特殊分布情况
        if abs(c - 1.0) < 0.01:
            print("→ 近似伽马分布 (c≈1)")
        elif abs(a - 1.0) < 0.01:
            print("→ 近似威布尔分布 (a≈1)")
        elif abs(c - 2.0) < 0.01 and abs(a - 0.5) < 0.01:
            print("→ 近似半正态分布")
        elif abs(c + 1.0) < 0.01:
            print("→ 近似倒伽马分布 (c≈-1)")
    
    except RuntimeError as e:
        print(f"拟合错误: {str(e)}")
    
