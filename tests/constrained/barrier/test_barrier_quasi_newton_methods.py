import numpy as np
import pytest

from nlinprog.constrained.barrier.quasi_newton import BarrierQuasiNewtonMethod
from tests.constrained.constrained_test_functions import (
    CONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS,
    ConstrainedOptimizationTestFunction)

BARRIER_TEST_FUNCTIONS = [
    func
    for func in CONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS
    if func.min_not_on_boundary and not func.h
]


@pytest.mark.parametrize("func", BARRIER_TEST_FUNCTIONS)
@pytest.mark.parametrize("line_search_method", ["wolfe", "armijo"])
@pytest.mark.parametrize("inverse_hessian_method", ["exact", "bfgs", "dfp", "broyden"])
@pytest.mark.parametrize("atol", [1e-4])
def test_barrier_newton_sovlers_grad_atol(
    func: ConstrainedOptimizationTestFunction,
    line_search_method,
    inverse_hessian_method,
    atol,
):
    solver = BarrierQuasiNewtonMethod(
        f=func.f,
        g=func.g,
        line_search_method=line_search_method,
        inverse_hessian_method=inverse_hessian_method,
    )
    res = solver.solve(
        x_0=func.x_start, atol1=atol, atol2=atol**2, rtol1=atol, rtol2=atol**2
    )
    assert np.allclose(np.abs(res.func - func.f(func.x_min)), 0, atol=atol)
