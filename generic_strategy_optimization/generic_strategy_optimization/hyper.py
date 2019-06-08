# -*- coding: utf-8 -*-


from typing import Dict, Callable

def evaluate(objective: Callable, data_gen: Callable, space: Dict, neval: int = 500) -> Dict:
    from hyperopt import fmin, tpe
    from functools import partial

    assert callable(objective)
    assert callable(data_gen)
    assert isinstance(space, dict)

    best = fmin(
            fn=partial(objective, data_gen),
            space=space,
            algo=tpe.suggest,
            max_evals=neval,
            )
    return best
