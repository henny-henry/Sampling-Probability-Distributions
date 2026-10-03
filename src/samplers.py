"""Sampling routines used by the probability-distribution experiments."""
import math
import numpy as np


def uniform(a, b, size):
    if b <= a:
        raise ValueError("The upper bound must exceed the lower bound.")
    return a + (b - a) * np.random.random(size)


def exponential(rate, size):
    if rate <= 0:
        raise ValueError("rate must be positive")
    return -np.log1p(-np.random.random(size)) / rate


def negative_binomial(p, successes, size):
    """Count failures before the requested successes, without a trial cutoff.

    Each inverse-transform draw counts failures before one success; independent
    geometric waiting times sum to a negative-binomial sample.
    """
    if not 0 < p <= 1:
        raise ValueError("p must lie in (0, 1]")
    if not isinstance(successes, (int, np.integer)) or successes < 1:
        raise ValueError("successes must be a positive integer")
    if p == 1:
        return np.zeros(size, dtype=int)
    failures = np.zeros(size, dtype=int)
    for _ in range(successes):
        failures += np.floor(
            np.log1p(-np.random.random(size)) / np.log1p(-p)
        ).astype(int)
    return failures


def generate_normal_box_muller(size):
    """Return exactly size standard-normal draws, including odd sample counts."""
    pairs = (size + 1) // 2
    # 1-U lies in (0, 1], so log never receives zero.
    radius = np.sqrt(-2 * np.log1p(-np.random.random(pairs)))
    angle = 2 * np.pi * np.random.random(pairs)
    return np.concatenate((radius * np.cos(angle), radius * np.sin(angle)))[:size]


def gamma_rejection(shape, rate, size, proposal_rate=0.5):
    """Gamma(shape, rate) draws using an exponential rejection envelope.

    This envelope requires shape > 1 and 0 < proposal_rate < rate. Its
    maximum occurs at (shape - 1)/(rate - proposal_rate), so no arbitrary
    finite optimization interval is needed. Return samples and run metadata.
    """
    if shape <= 1 or not 0 < proposal_rate < rate:
        raise ValueError("Require shape > 1 and 0 < proposal_rate < rate")
    mode = (shape - 1) / (rate - proposal_rate)

    def log_ratio(x):
        return (
            shape * math.log(rate) - math.lgamma(shape)
            - math.log(proposal_rate) + (shape - 1) * math.log(x)
            - (rate - proposal_rate) * x
        )

    log_envelope = log_ratio(mode) + math.log(1.05)
    samples = np.empty(size)
    accepted = proposals = 0
    while accepted < size:
        candidate = float(exponential(proposal_rate, 1)[0])
        proposals += 1
        if candidate > 0 and np.random.random() <= math.exp(log_ratio(candidate) - log_envelope):
            samples[accepted] = candidate
            accepted += 1
    return samples, {"envelope": math.exp(log_envelope), "proposals": proposals}
