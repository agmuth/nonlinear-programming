from typing import Union

import numpy as np


class ConstrainedOptimizationTestFunction:
    def __init__(
        self,
        f: callable,
        g: Union[callable, None],
        h: Union[callable, None],
        x_min: np.ndarray,
        x_start: np.ndarray,
    ):
        self.f = f
        self.g = g
        self.h = h
        self.x_min = x_min
        self.x_start = x_start

    @property
    def min_not_on_boundary(self):
        return np.all(self.g(self.x_min) < 0) if self.g else True


constrained_rosenbrock1 = ConstrainedOptimizationTestFunction(
    # rosenbroack constrained by cubiic and line
    f=lambda x: (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2,
    g=lambda x: np.array([(x[0] - 1) ** 3 - x[1] + 1, x.sum() - 2]),
    h=None,
    x_start=np.array([2.0, -0.5]),
    x_min=np.ones(2),
)

constrained_rosenbrock2 = ConstrainedOptimizationTestFunction(
    # rosenbrock constrained to a disk
    f=lambda x: (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2,
    g=lambda x: np.array([np.square(x).sum() - 2.5]),
    h=None,
    x_start=np.array([-0.5, -0.5]),
    x_min=np.ones(2),
)

constrained_rosenbrock3 = ConstrainedOptimizationTestFunction(
    # rosenbrock constrained to a disk and to a line
    f=lambda x: (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2,
    g=lambda x: np.array([np.square(x).sum() - 2.5]),
    h=lambda x: np.array([x[0] - x[1]]),
    x_start=np.array([1.0, -1.0]),
    x_min=np.ones(2),
)

maytas1 = ConstrainedOptimizationTestFunction(
    # maytas constrained to a sine wave on the unit disk
    f=lambda x: 0.26 * np.square(x).sum() - 0.48 * np.prod(x),
    g=lambda x: np.array([np.square(x).sum() - 1]),
    h=lambda x: np.array(
        [
            np.sin(x[0]),
            np.sin(x[1]),
        ]
    ),
    x_start=np.array([10.0, -10.0]),
    x_min=np.zeros(2),
)

CONSTRAINED_OPTIMIZATION_TEST_FUNCTIONS = [
    x[1]
    for x in globals().items()
    if isinstance(x[1], ConstrainedOptimizationTestFunction)
]
