#!/usr/bin/env python3
# v1.2-Refactor: Integration Test
"""
Integration Test for v1.2 LPL/PCM/PGI Systems
==============================================

Tests that all three subsystems work together correctly.

Addendum v1.2 Section: Integration Testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from lpl_utilities import LPL_Graph, Condition, LPL_build_graph
from pcm_operators import PCM_Processor, PCM_safe_contradiction
from pgi_metrics import PGI_Tracker
import numpy as np

def test_integration():
    """
    Integration test: LPL → PCM → PGI pipeline.
    
    Simulates a system detecting violations, metabolizing contradictions,
    and tracking generative evolution.
    """
    print("=" * 70)
    print("v1.2 Integration Test: LPL → PCM → PGI Pipeline")
    print("=" * 70)
    
    # Step 1: LPL - Build dependency graph
    print("\n[Step 1: LPL] Building dependency graph...")
    conditions = [
        Condition("C1", "Ontological", "Existence", set(), 0),
        Condition("C2", "Ontological", "Identity", {"C1"}, 1),
        Condition("C13", "Logical-Formal", "Non-Contradiction", {"C2"}, 2),
    ]
    lpl_graph = LPL_build_graph(conditions)
    print(f"✓ LPL graph built with {len(lpl_graph.vertices)} conditions")
    
    presups = lpl_graph.LPL_find_presuppositions("C13")
    print(f"✓ Presuppositions for C13: {presups}")
    
    # Step 2: PCM - Detect and metabolize contradictions
    print("\n[Step 2: PCM] Metabolizing contradictions...")
    pcm = PCM_Processor(lambda_rate=0.8, epsilon=0.01)
    
    # Simulate violations of conditions (with decreasing severity)
    violations = [
        ("C13", 0.9),  # Non-contradiction violation (severe)
        ("C2", 0.7),   # Identity violation (medium)
        ("C2", 0.5),   # Identity violation (low)
        ("C13", 0.3),  # Non-contradiction violation (resolved)
    ]
    
    for cond_id, severity in violations:
        sat = PCM_safe_contradiction(
            f"holds({cond_id})",
            f"¬holds({cond_id})",
            {"severity": severity, "condition": cond_id}
        )
        g_state = pcm.PCM_metabolize(sat)
        print(f"✓ Metabolized {cond_id} (severity={severity:.2f}) → G^{g_state.generative_rank}")
        
        if g_state.blooms:
            print(f"  → Bloom triggered: {g_state.blooms[0]}")
    
    # Check convergence
    is_converging, lambda_est = pcm.PCM_check_convergence()
    print(f"✓ PCM convergence: λ={lambda_est:.3f} (< 1.0: {is_converging})")
    
    # Step 3: PGI - Track generative evolution
    print("\n[Step 3: PGI] Tracking generative evolution...")
    pgi_tracker = PGI_Tracker()
    
    # Simulate system evolution over time
    for t in range(5):
        # Coherence improves as contradictions are metabolized
        coherence_scores = np.random.rand(3) * 0.3 + 0.6 + t * 0.05
        
        system_state = {
            'coherence_scores': coherence_scores,
            'transformations_per_time': t * 0.1,
            'timestamp': t
        }
        
        pgi = pgi_tracker.PGI_compute(system_state)
        print(f"✓ t={t}: PGI={pgi.total_pgi():.4f}")
    
    # Verify conservation law
    is_conserved, deltas = pgi_tracker.PGI_verify_conservation()
    print(f"✓ PGI Conservation (dXGI/dt ≥ 0): {is_conserved}")
    
    # Step 4: Integration verification
    print("\n[Step 4: Integration] Verifying complete pipeline...")
    
    checks = {
        "LPL graph valid": len(lpl_graph.vertices) > 0,
        "PCM converging": is_converging,
        "PGI conserved": is_conserved,
        "Dependencies tracked": len(presups) > 0,
        "Contradictions metabolized": len(pcm.history) > 0,
        "Generativity measured": len(pgi_tracker.history) > 0,
    }
    
    print("\nIntegration Checks:")
    all_passed = True
    for check, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {check}: {status}")
        all_passed = all_passed and passed
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All integration tests PASSED")
        print("v1.2 LPL/PCM/PGI systems are functioning correctly.")
    else:
        print("✗ Some integration tests FAILED")
        return 1
    
    print("=" * 70)
    return 0

if __name__ == "__main__":
    exit_code = test_integration()
    sys.exit(exit_code)
