#!/usr/bin/env python3
"""Minimal CFPE GNN demo
This script implements a simplified numeric demo of the CFPE Generative Neural Network
as described in the CFPE formalism document. It is intentionally small and deterministic
so it can run in this environment quickly and produce human-readable output.

Produces: per-iteration logs of Generativity (G), dG, and XGI.
"""
import numpy as np

np.random.seed(42)

# Problem size & hyperparams
N_COHERENCE = 3  # number of coherence functions / invariants
THRESHOLD_SAT = 0.8
MAX_ITERS = 50
ETA = 0.05         # learning rate for parameters (theta)
ETA_META = 0.01    # meta-learning rate for penalties/weights

# Initialize neural parameters theta
D = 8
theta = np.random.randn(D) * 0.1

# Feature vectors v_i that map theta -> z_i
V = np.random.randn(N_COHERENCE, D)
B = np.random.randn(N_COHERENCE) * 0.01  # biases

# Importance weights p_i and dissipation penalties a_j
p = np.ones(N_COHERENCE) / N_COHERENCE
a = np.array([5.0, 5.0, 5.0])  # initial penalties

# Meta-update prototypes w_k for contradiction detection
K = 3
W_meta = np.eye(N_COHERENCE)  # use simple identity prototypes
b_meta = np.full(K, 0.2)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def smooth_sigmoid(x, kappa=10.0):
    return 1.0 / (1.0 + np.exp(-kappa * (1 - x)))  # maps C to near 1 when C>~0.9

# Utility: coherence functions C_i(theta)
def compute_C(theta):
    z = V.dot(theta) + B
    C = sigmoid(z)
    return C, z

# Generativity function
# G = sum p_i log(C_i) + log(n) - sum a_j Delta_j^2
# where Delta_j = max(0, 1 - C_j)
def compute_generativity(C):
    eps = 1e-9
    coherence_info = np.sum(p * np.log(np.clip(C, eps, 1.0)))
    n = np.sum(C > THRESHOLD_SAT)
    expansion = np.log(n + 1.0)
    Delta = np.maximum(0.0, 1.0 - C)
    dissipation = np.sum(a * (Delta ** 2))
    G = coherence_info + expansion - dissipation
    return G, Delta, n

# Gradient wrt theta (analytic for this simple model)
# dC/dtheta = sigmoid'(z) * V_i
# grad_G = sum_i p_i/C_i * dC_i + 2 * sum_j a_j * Delta_j * dC_j (only when C_j<1)
def grad_generativity(theta, C, z, Delta):
    sigma_prime = sigmoid(z) * (1 - sigmoid(z))
    dC_dtheta = (sigma_prime[:, None] * V)
    term1 = np.sum((p / np.clip(C, 1e-9, 1.0))[:, None] * dC_dtheta, axis=0)
    # Delta_j derivative: d(Delta_j) = -dC_j when C_j < 1
    mask = (C < 1.0).astype(float)
    term2 = 2.0 * np.sum(((a * Delta * mask)[:, None]) * dC_dtheta, axis=0)
    grad = term1 + term2
    return grad

# XGI smooth form
def compute_XGI(C):
    s = sigmoid(10.0 * (C - 0.5))  # smooth approx of satisfaction
    return np.mean(s)

# Metabolic operator Omega_0 (very small demo): adjust penalties a
# For the largest contradiction, slightly reduce penalty to allow exploration
# Also produce a correction Psi (vector) that could be applied to theta (here small)
def Omega_0(Delta, theta):
    # classify highest violation
    idx = np.argmax(Delta)
    Psi = -0.1 * Delta  # small damping vector (applied uniformly per-invariant)
    # rule revision: slightly relax penalty of the most violated invariant
    a_update = np.zeros_like(a)
    a_update[idx] = -0.2 * a[idx]
    return a_update, Psi

# Meta-update operator M: produce additive modification to G via basis functions
# We'll let it slightly increase p for invariants that are improving
def M_meta(Delta):
    lambdas = sigmoid(np.dot(W_meta, Delta) - b_meta)
    # three phi modes: boost coherence_info, reduce dissipation, increase expansion potential
    phi1 = 0.1 * np.log(1.0 + np.linalg.norm(Delta))
    phi2 = -0.05 * np.sum(Delta ** 2)
    phi3 = 0.05 * np.log(1.0 + np.sum(Delta > 0.05))
    # Compose
    mods = np.array([phi1, phi2, phi3])
    deltaG = np.dot(lambdas, mods)
    return deltaG, lambdas

# Training loop
log_lines = []
G_prev = None
for t in range(MAX_ITERS):
    C, z = compute_C(theta)
    G, Delta, n_sat = compute_generativity(C)
    XGI = compute_XGI(C)
    if G_prev is None:
        dG = 0.0
    else:
        dG = G - G_prev
    if t % 5 == 0 or t == MAX_ITERS - 1:
        line = f"t={t:03d} | G={G:.4f} | dG={dG:.4f} | XGI={XGI:.4f} | C={C.round(3).tolist()} | a={a.round(3).tolist()}"
        print(line)
        log_lines.append(line)
    # Metabolic processing
    if np.max(Delta) > 0.1:
        a_delta, Psi = Omega_0(Delta, theta)
        a = np.clip(a + ETA_META * a_delta, 0.1, 50.0)
        # optional: apply Psi as small correction to theta
        theta = theta + 0.01 * np.sum(Psi)  # tiny scalar shift
    # Compute gradients and update theta (gradient ascent)
    grad = grad_generativity(theta, C, z, Delta)
    theta = theta + ETA * grad
    # Meta-update to G: we do not maintain symbolic G function in code; we simulate effect via p and a
    deltaG_mod, lambdas = M_meta(Delta)
    # Apply small meta effect: nudge p towards invariants with lower Delta
    p = p + ETA_META * (1.0 - Delta)
    p = np.clip(p, 1e-3, 10.0)
    p = p / np.sum(p)
    G_prev = G

# Final state print
C, z = compute_C(theta)
G, Delta, n_sat = compute_generativity(C)
XGI = compute_XGI(C)
final_line = f"FINAL | G={G:.4f} | XGI={XGI:.4f} | C={C.round(4).tolist()} | a={a.round(4).tolist()}"
print(final_line)
log_lines.append(final_line)

# Write the run output to a file inside the repository for later insertion into the markdown
out_path = '/workspaces/Summa-Generativarum/tools/output_cfpe_gnn_run.txt'
try:
    with open(out_path, 'w') as f:
        for ln in log_lines:
            f.write(ln + '\n')
except Exception as e:
    # If writing fails, emit a warning to stdout but continue
    print(f"Warning: failed to write run output to {out_path}: {e}")

# Also print a short summary
print('\n[Demo complete] Logged lines written to /workspace_cfpe_gnn_run_output.txt')
