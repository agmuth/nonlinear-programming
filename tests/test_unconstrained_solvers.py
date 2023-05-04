import numpy as np
import pytest

from nlinprog.unconstrained.unconstrained_solvers import QuasiNewtonMethod, ConjugateGradientMethod
from tests.test_functions import UNCONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS, UnconstrainedOptimizationTestFunction


@pytest.mark.parametrize("func", UNCONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS[:-1])
@pytest.mark.parametrize("line_search_method", ["wolfe", "armijo"])
@pytest.mark.parametrize("inverse_hessian_method", ["exact", "bfgs", "dfp", "broyden"])
@pytest.mark.parametrize("atol", [1e-4])
def test_newton_sovlers_grad_atol(
        func: UnconstrainedOptimizationTestFunction, 
        line_search_method,
        inverse_hessian_method, 
        atol,
    ):
    solver = QuasiNewtonMethod(f=func.f, line_search_method=line_search_method, inverse_hessian_method=inverse_hessian_method)
    res = solver.solve(x_0=func.x_start, grad_atol=atol)

    # check that L2 norm of grad is same order of magnitude as atol - some methods do not garuantee that grad is monotonic decreasing. 
    assert np.allclose(np.logaddexp(np.linalg.norm(res.grad), atol), 0.0, atol=10) and res.converged


@pytest.mark.parametrize("func", UNCONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS[:-1])
@pytest.mark.parametrize("line_search_method", ["armijo", "wolfe"])
@pytest.mark.parametrize("conjugate_gradient_direction_method", ["polak-ribier", "fletcher-reeves"])
@pytest.mark.parametrize("atol", [1e-4])
def test_conjugate_gradient_sovlers_grad_atol(
        func: UnconstrainedOptimizationTestFunction, 
        line_search_method,
        conjugate_gradient_direction_method, 
        atol,
    ):
    solver = ConjugateGradientMethod(f=func.f, line_search_method=line_search_method, conjugate_gradient_direction_method=conjugate_gradient_direction_method)
    res = solver.solve(x_0=func.x_start, grad_atol=atol)

    # check that L2 norm of grad is same order of magnitude as atol - some methods do not garuantee that grad is monotonic decreasing. 
    assert np.allclose(np.logaddexp(np.linalg.norm(res.grad), atol), 0.0, atol=10) and res.converged
    
    