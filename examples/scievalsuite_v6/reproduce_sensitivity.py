import numpy as np
from scipy.stats import friedmanchisquare, rankdata

# Curated 6-task data, 3 local models (7b, 14b, gemma), per compute_curated_friedman.py
# raw metrics: Sentiment, TextSim, TextClass, Zinc(MAE), MathQA, FinQA
raw_7b = [0, 0, 0, 0, 0, 0]
raw_14b = [0, 0, 0.6252, 1.5422, 0, 0]
raw_gemma = [0.2, 0.533, 0, 0, 0, 0]
is_acc = [True, True, True, False, True, True]

def transform(raw):
    # accuracy/correlation -> -raw (higher better -> lower rank), MAE -> raw (lower better)
    return [-r if is_acc[i] else r for i, r in enumerate(raw)]

t7b = transform(raw_7b)
t14b = transform(raw_14b)
tgem = transform(raw_gemma)

print('transformed:')
print(' 7b:  ', t7b)
print(' 14b: ', t14b)
print(' gemma:', tgem)

# fail=-10 (fail as worst): Zinc fail -> -10 (MAE, higher is worse)
raw_7b_w = [0, 0, 0, -10, 0, 0]
raw_14b_w = [0, 0, 0.6252, -1.5422, 0, 0]
raw_gemma_w = [0.2, 0.533, 0, -10, 0, 0]
t7b_w = transform(raw_7b_w)
t14b_w = transform(raw_14b_w)
tgem_w = transform(raw_gemma_w)

def friedman(a, b, c, label):
    chi2, p = friedmanchisquare(a, b, c)
    print('%-40s chi2=%.4f p=%.4f' % (label, chi2, p))
    return chi2, p

print()
friedman(t7b_w, t14b_w, tgem_w, 'fail=-10 (worst):')
friedman(t7b, t14b, tgem, 'fail=0 (best):')

# fail=NaN (exclude): try excluding tasks where ANY model is 0 (fail)
print()
print('--- fail=NaN attempts ---')
# Interpretation 1: exclude tasks where any model failed (score 0)
keep = [i for i in range(6) if all(x != 0 for x in [raw_7b[i], raw_14b[i], raw_gemma[i]])]
print('tasks kept (all non-fail):', keep)
if len(keep) >= 3:
    friedman([t7b[i] for i in keep], [t14b[i] for i in keep], [tgem[i] for i in keep], 'exclude any-fail tasks:')

# Interpretation 2: per-model exclude failed values (unequal N) - use only non-zero per model
for mname, arr in [('7b', t7b), ('14b', t14b), ('gemma', tgem)]:
    nz = [v for v in arr if v != 0]
    print('  %s non-zero values: %s' % (mname, nz))

# Interpretation 3: exclude tasks where the model failed, but require >=3 common tasks
# (7b fails all, so no common tasks)
common = [i for i in range(6) if raw_7b[i] != 0 and raw_14b[i] != 0 and raw_gemma[i] != 0]
print('common non-fail tasks:', common)

# Interpretation 4: maybe k=3 is 14b, gemma, curated-frontier (max(14b,gemma))
raw_cur = [0.2, 0.533, 0.6252, 1.5422, 0, 0]
tcur = transform(raw_cur)
friedman(t14b, tgem, tcur, '14b/gemma/cur fail=0:')
raw_cur_w = [0.2, 0.533, 0.6252, -1.5422, 0, 0]
tcur_w = transform(raw_cur_w)
friedman(t14b_w, tgem_w, tcur_w, '14b/gemma/cur fail=-10:')

# Interpretation 5: 7b, 14b, gemma with fail=NaN but only on Zinc (exclude Zinc entirely)
keep2 = [i for i in range(6) if i != 3]  # exclude Zinc
friedman([t7b[i] for i in keep2], [t14b[i] for i in keep2], [tgem[i] for i in keep2], 'exclude Zinc task:')
