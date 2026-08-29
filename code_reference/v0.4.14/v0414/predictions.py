from __future__ import annotations

import math
from typing import Iterable


def sigmoid(value: float) -> float:
    if value >= 0:
        factor = math.exp(-value)
        return 1.0 / (1.0 + factor)
    factor = math.exp(value)
    return factor / (1.0 + factor)


def predicted_probability(delta: float, temperature: float) -> float:
    if temperature <= 0:
        raise ValueError("La température doit être strictement positive.")
    return sigmoid(delta / temperature)


def binomial_cdf(k: int, n: int, probability: float) -> float:
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Probabilité hors de [0, 1].")
    if probability == 0.0:
        return 1.0
    if probability == 1.0:
        return 0.0
    return sum(
        math.comb(n, value)
        * probability**value
        * (1.0 - probability) ** (n - value)
        for value in range(k + 1)
    )


def central_predictive_range(
    n: int,
    probability: float,
    *,
    two_sided_alpha: float,
) -> tuple[int, int]:
    if not 0.0 < two_sided_alpha < 1.0:
        raise ValueError("Alpha doit appartenir à ]0, 1[.")
    tail = two_sided_alpha / 2.0
    lower = next(k for k in range(n + 1) if binomial_cdf(k, n, probability) >= tail)
    upper = next(
        k for k in range(n + 1)
        if binomial_cdf(k, n, probability) >= 1.0 - tail
    )
    return lower, upper


def _bisect_decreasing(function, target: float) -> float:
    low, high = 0.0, 1.0
    for _ in range(80):
        middle = (low + high) / 2.0
        if function(middle) > target:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def clopper_pearson(
    successes: int,
    trials: int,
    *,
    confidence: float = 0.95,
) -> tuple[float, float]:
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("Comptage binomial invalide.")
    if not 0.0 < confidence < 1.0:
        raise ValueError("Niveau de confiance invalide.")
    tail = (1.0 - confidence) / 2.0

    if successes == 0:
        lower = 0.0
    else:
        lower = _bisect_decreasing(
            lambda p: binomial_cdf(successes - 1, trials, p),
            1.0 - tail,
        )

    if successes == trials:
        upper = 1.0
    else:
        upper = _bisect_decreasing(
            lambda p: binomial_cdf(successes, trials, p),
            tail,
        )
    return lower, upper


def mean(values: Iterable[float]) -> float | None:
    materialized = list(values)
    if not materialized:
        return None
    return sum(materialized) / len(materialized)
