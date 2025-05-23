import math
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scipy.stats import chi2

class Chi2Request(BaseModel):
    x: float
    df: float = 1.0
    lower_tail: bool = False

app = FastAPI()

@app.post("/chi2_scipy", response_model=List[float])
async def chi2_scipy(requests: List[Chi2Request]):
    """SciPy-based chi-square CDF endpoint"""
    results = []
    for req in requests:
        if req.df <= 0:
            raise HTTPException(status_code=400, detail="Degrees of freedom (df) must be positive")
        if req.x < 0:
            raise HTTPException(status_code=400, detail="x must be non-negative for chi-square distribution")
        cdf_val = chi2.cdf(req.x, req.df)
        prob = cdf_val if req.lower_tail else (1 - cdf_val)
        results.append(prob)
    return results

# Pure-Python implementation of the regularized lower incomplete gamma function
from math import exp, log, lgamma

def _lower_gamma_reg(a: float, x: float, eps: float = 1e-12, max_iter: int = 1000) -> float:
    if x < 0 or a <= 0:
        raise ValueError("Invalid arguments for lower incomplete gamma")
    # Series representation for x < a+1
    if x < a + 1:
        term = 1.0 / a
        sum_ = term
        for n in range(1, max_iter):
            term *= x / (a + n)
            sum_ += term
            if term < eps * sum_:
                break
        return sum_ * exp(-x + a * log(x) - lgamma(a))
    # Continued fraction for complement Q(a, x)
    fpmin = 1e-300
    b = x + 1 - a
    c = 1 / fpmin
    d = 1 / b
    h = d
    for i in range(1, max_iter):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        if abs(d) < fpmin:
            d = fpmin
        c = b + an / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    q = exp(-x + a * log(x) - lgamma(a)) * h
    return 1 - q

@app.post("/chi2_probabilities", response_model=List[float])
async def chi2_pure(requests: List[Chi2Request]):
    """Pure-Python chi-square CDF endpoint"""
    results = []
    for req in requests:
        if req.df <= 0:
            raise HTTPException(status_code=400, detail="Degrees of freedom (df) must be positive")
        if req.x < 0:
            raise HTTPException(status_code=400, detail="x must be non-negative for chi-square distribution")
        cdf_val = _lower_gamma_reg(req.df / 2, req.x / 2)
        prob = cdf_val if req.lower_tail else (1 - cdf_val)
        results.append(prob)
    return results 