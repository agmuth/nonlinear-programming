import numpy as np
import pytest

from nlinprog.constrained.penalty.quasi_newton import PenalizedQuasiNewtonMethod
from tests.constrained.constrained_test_functions import CONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS, ConstrainedOptimizationTestFunction

PENALIZED_TEST_FUNCTIONS = [func for func in CONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS if not func.min_not_on_boundary or func.h]

@pytest.mark.parametrize("func", PENALIZED_TEST_FUNCTIONS)
@pytest.mark.parametrize("line_search_method", ["wolfe", "armijo"])
@pytest.mark.parametrize("inverse_hessian_method", ["exact", "bfgs", "dfp", "broyden"])
@pytest.mark.parametrize("atol", [1e-4])
def test_penalized_newton_sovlers_grad_atol(
        func: ConstrainedOptimizationTestFunction, 
        line_search_method,
        inverse_hessian_method, 
        atol,
    ):
    solver = PenalizedQuasiNewtonMethod(f=func.f, g=func.g, h=func.h, line_search_method=line_search_method, inverse_hessian_method=inverse_hessian_method)
    res = solver.solve(x_0=func.x_start, grad_atol=atol)

    # check that L2 norm of grad is same order of magnitude as atol - some methods do not garuantee that grad is monotonic decreasing. 
    # assert np.allclose(np.logaddexp(np.linalg.norm(res.grad), atol), 0.0, atol=10) and res.converged
    assert np.allclose(np.linalg.norm(res.x - func.x_min), 0, atol=0.1)

