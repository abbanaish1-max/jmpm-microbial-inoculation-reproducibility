#!/usr/bin/env python3
"""Reproduce the scalar fractional numerical checks reported in the manuscript.

This script does NOT reproduce the secondary-data workbook analysis or ML benchmark.
It reproduces only: (i) constant-order Caputo L1 relaxation; (ii) a selected
terminal-time variable-order endpoint refinement; (iii) a manufactured-solution
test for x*(t)=t^2; and (iv) a hand-checkable study-first aggregation example.

Run: python numerical_validation.py --output-dir outputs
Requires: mpmath >= 1.3
"""
from __future__ import annotations
import argparse
import csv
import math
from pathlib import Path
from typing import Iterable
import mpmath as mp


def mittag_leffler_e_alpha(alpha: float, z: float, tol: str = "1e-45", min_terms: int = 11) -> mp.mpf:
    """Compute E_alpha(z)=sum_{k>=0} z^k/Gamma(alpha*k+1) at high precision."""
    with mp.workdps(50):
        a = mp.mpf(str(alpha))
        zz = mp.mpf(str(z))
        tol_mp = mp.mpf(tol)
        total = mp.mpf('0')
        for k in range(1000):
            term = (zz ** k) / mp.gamma(a * k + 1)
            total += term
            if k + 1 >= min_terms and abs(term) < tol_mp:
                break
        else:
            raise RuntimeError("Mittag-Leffler series did not meet the tolerance in 1000 terms")
        return +total


def l1_constant_order(alpha: float, kappa: float, x0: float, T: float, N: int) -> tuple[list[float], list[float]]:
    """Implicit uniform-grid L1 scheme for D_C^alpha x = -kappa*x."""
    dt = T / N
    x = [0.0] * (N + 1)
    x[0] = x0
    times = [n * dt for n in range(N + 1)]
    for n in range(1, N + 1):
        c = dt ** (-alpha) / math.gamma(2.0 - alpha)
        history = 0.0
        for j in range(1, n):
            w = (j + 1) ** (1.0 - alpha) - j ** (1.0 - alpha)
            history += w * (x[n-j] - x[n-j-1])
        x[n] = (c * x[n-1] - c * history) / (c + kappa)
    return times, x


def run_constant_order() -> list[dict[str, float | int | str]]:
    rows=[]
    kappa=0.55; x0=1.0; T=1.0
    for alpha in (0.55, 0.72, 0.90):
        exact = float(x0 * mittag_leffler_e_alpha(alpha, -kappa * T**alpha))
        errors={}
        numerics={}
        for N in (20,40,80,160,320,640):
            _, x = l1_constant_order(alpha,kappa,x0,T,N)
            numerics[N]=x[-1]
            errors[N]=abs(x[-1]-exact)
        for N in (20,40,80,160,320,640):
            rate = math.log(errors[N]/errors[2*N],2) if 2*N in errors else None
            rows.append({"alpha":alpha,"N":N,"dt":T/N,"x_numeric_T":numerics[N],
                         "x_exact_T":exact,"absolute_error_T":errors[N],
                         "observed_p_N":"" if rate is None else rate})
    return rows


def variable_order_endpoint(N: int, T: float = 2.0, kappa: float = 0.55) -> float:
    """Endpoint of D^VO x=-kappa*x, alpha(t)=0.70+0.12 sin(pi*t), x(0)=1."""
    dt=T/N
    x=[0.0]*(N+1); x[0]=1.0
    for n in range(1,N+1):
        t=n*dt
        alpha=0.70+0.12*math.sin(math.pi*t)
        c=dt**(-alpha)/math.gamma(2.0-alpha)
        history=0.0
        for j in range(1,n):
            w=(j+1)**(1.0-alpha)-j**(1.0-alpha)
            history += w*(x[n-j]-x[n-j-1])
        x[n]=(c*x[n-1]-c*history)/(c+kappa)
    return x[-1]


def run_variable_order_endpoint() -> list[dict[str, float | int]]:
    Ns=(40,80,160,320,640)
    vals={N:variable_order_endpoint(N) for N in Ns}
    ref=vals[640]
    return [{"N":N,"dt":2.0/N,"x_T":vals[N],"abs_difference_from_N640":abs(vals[N]-ref)} for N in Ns]


def variable_order_manufactured(N: int) -> tuple[float,float,float,float]:
    """Manufactured solution x*(t)=t^2, alpha(t)=0.70+0.12 sin(pi*t), T=1."""
    T=1.0; dt=T/N
    x=[0.0]*(N+1)
    for n in range(1,N+1):
        t=n*dt
        alpha=0.70+0.12*math.sin(math.pi*t)
        c=dt**(-alpha)/math.gamma(2.0-alpha)
        forcing=math.gamma(3.0)*t**(2.0-alpha)/math.gamma(3.0-alpha)
        history=0.0
        for j in range(1,n):
            w=(j+1)**(1.0-alpha)-j**(1.0-alpha)
            history += w*(x[n-j]-x[n-j-1])
        x[n]=x[n-1]+forcing/c-history
    errors=[abs(x[n]-(n*dt)**2) for n in range(N+1)]
    return max(errors), abs(x[-1]-1.0), x[-1], 1.0


def run_variable_order_manufactured() -> list[dict[str, float | int | str]]:
    Ns=(20,40,80,160,320,640)
    vals={N:variable_order_manufactured(N) for N in Ns}
    rows=[]
    for N in Ns:
        emax,eend,xT,xstar=vals[N]
        rate=math.log(emax/vals[2*N][0],2) if 2*N in vals else None
        rows.append({"N":N,"dt":1.0/N,"max_abs_error":emax,
                     "endpoint_abs_error":eend,"numerical_x_T":xT,"exact_x_T":xstar,
                     "observed_order_max_error":"" if rate is None else rate})
    return rows


def study_first_aggregation_unit_test() -> float:
    """Two rows in each of two studies: means .15 and .95; equal-study mean .55."""
    groups={"study_A":[0.10,0.20],"study_B":[0.90,1.00]}
    study_means=[sum(v)/len(v) for v in groups.values()]
    return sum(study_means)/len(study_means)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',default='outputs')
    args=ap.parse_args()
    out=Path(args.output_dir)
    write_csv(out/'constant_order_L1_recomputed.csv',run_constant_order())
    write_csv(out/'variable_order_endpoint_recomputed.csv',run_variable_order_endpoint())
    write_csv(out/'variable_order_manufactured_recomputed.csv',run_variable_order_manufactured())
    agg=study_first_aggregation_unit_test()
    print(f"Study-first aggregation unit test: {agg:.12f} (expected 0.55)")
    if not math.isclose(agg,0.55,rel_tol=0,abs_tol=1e-12):
        raise AssertionError('Study-first aggregation unit test failed')
    print(f"Wrote numerical test results to: {out.resolve()}")

if __name__=='__main__':
    main()
