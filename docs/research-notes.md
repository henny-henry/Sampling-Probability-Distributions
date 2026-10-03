# Research provenance and reproducibility

The report is the primary account of the research. Its scientific content and all original figure files are retained. Only the student identifier and PDF metadata were removed for public presentation. Original pre-cleanup files are backed up outside this repository in the local workspace.

## Differences retained

- The report describes Bernoulli sums for binomial, sequential Bernoulli trials for geometric/negative binomial, and random permutations for hypergeometric sampling. The final notebook instead calls built-in NumPy samplers for those four distributions. Earlier manual implementations remain in `sampling_exploration.ipynb`.
- The report defines geometric samples as failures before success (support starting at zero); both notebook versions use a trials-until-success convention (support starting at one), via different methods. Do not directly compare these without adjusting the convention.
- Parameters differ across versions: the final notebook uses binomial `p=0.51`, while the exploration uses `p=0.3`. The report's binomial caption says `p=3`, an apparent typographical error. No research parameters were changed to reconcile these.
- The exploratory negative-binomial sampler stops after 50 trials and retains incomplete samples; its stored warning reports 73 incomplete draws out of 10,000. It also reads a global sample count instead of its argument and has copied geometric plot labels. This potentially biased exploratory result is preserved, not silently corrected.
- The report describes a search for the rejection envelope; code uses bounded scalar optimization on `(1e-6, 100)` and a 5% margin. This is an experiment at the supplied parameters, not a validated general-purpose gamma sampler for every positive shape/rate.
- Beta and Poisson code uses NumPy gamma/exponential draws. The implementation therefore does not construct every distribution exclusively from primitive uniform draws.
- The original Box–Muller function returns `2 * (N // 2)` samples; the experiment's even `N=10000` works as intended. Odd sample counts would be shortened.
- The report has incomplete/mislabeled figure captions. The original figures and conclusions have not been rewritten.

## Engineering changes

- Fixed the final notebook's `plot_bar` signature: an unused `bins` argument made the existing calls fail. Removed that unused keyword from the Poisson call.
- Fixed the uniform plot's undefined `uni_samples` reference to use the actual generated `samples`.
- Removed a duplicated normal histogram, added descriptive section headings, and removed empty cells and local warning output.
- Replaced the exploratory notebook's removed `np.math` alias with standard-library `math`; no formula changed.
- Preserved stored scientific outputs. Execution fixes may change newly rendered plots relative to stale notebook state. No claim is made that stored outputs were produced by the exact saved source in a fresh kernel.
- Removed the redundant HTML notebook export. The PDF and both substantively different notebooks remain.

The dependency file describes a compatible environment, not an original lockfile. Seed 42 is present only in the final notebook; the exploration is unseeded. Library versions and random-number consumption affect exact realizations. Visual agreement is the project's evidence; confidence intervals, goodness-of-fit tests, mixing diagnostics, and runtime comparisons would be extensions.

## Validation

Both notebooks were validated with nbformat and all code cells executed sequentially in fresh Python 3.11 processes (NumPy 1.25.2, SciPy 1.11.1, Matplotlib 3.7.2, pandas 2.1.2). Figures were rendered with a noninteractive backend; saved historical outputs were not overwritten. The final rerun accepted 10,000 of 27,354 proposals (36.6%), illustrating why historical values are labeled separately. The exploratory sampler still emits its documented incomplete-trial warning.
