#!/usr/bin/env python3
# v1.2-Refactor: aligned with Addendum v1.2 (Non-Destructive Update)
"""
PGI (Phenomenological Generativity Index) Metrics - v1.2
=========================================================

Quantifies generative capacity and complexity evolution.

Key Functions:
- PGI_compute(system_state): Calculate current generativity
- PGI_delta(state_t, state_t1): Compute ΔG_t
- PGI_compression_ratio(data): Kolmogorov complexity proxy
- PGI_entropy_estimate(distribution): Shannon entropy
- PGI_track_evolution(history): Plot generativity trajectory
- PGI_verify_conservation(): Check dXGI/dt ≥ 0

Formal Definition:
    PGI(S, t) := ⟨G_rate, CO, S_div, Conn, Adopt, Res⟩
    where:
      G_rate: Novel transformations per time unit
      CO: Constraint openness (0-1 scale)
      S_div: Substrate diversity
      Conn: Network connectivity
      Adopt: Adoption rate of new structures
      Res: Resilience to perturbation

Generativity Change:
    ΔG_t = PGI(S, t+1) - PGI(S, t)
    Conservation Law: dXGI_total/dt ≥ 0

Addendum v1.2 Section: PGI.1.1
Author: PROMETHIVM LLC
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np
import zlib

@dataclass
class PGI_State:
    """
    Phenomenological Generativity Index state.
    
    Addendum v1.2 Section: PGI.1.2
    """
    G_rate: float  # Novel transformations per time unit
    CO: float  # Constraint openness [0, 1]
    S_div: float  # Substrate diversity
    Conn: float  # Network connectivity
    Adopt: float  # Adoption rate
    Res: float  # Resilience
    timestamp: float
    
    def total_pgi(self) -> float:
        """
        Compute aggregate PGI score.
        
        Weighted sum of components.
        """
        weights = {
            'G_rate': 0.25,
            'CO': 0.15,
            'S_div': 0.15,
            'Conn': 0.15,
            'Adopt': 0.15,
            'Res': 0.15
        }
        
        return (
            weights['G_rate'] * self.G_rate +
            weights['CO'] * self.CO +
            weights['S_div'] * self.S_div +
            weights['Conn'] * self.Conn +
            weights['Adopt'] * self.Adopt +
            weights['Res'] * self.Res
        )


class PGI_Tracker:
    """
    Track and analyze Phenomenological Generativity Index evolution.
    
    Addendum v1.2 Section: PGI.2.1
    LEGACY: XGI_tracker from v1.1
    """
    
    def __init__(self):
        """Initialize PGI tracker."""
        self.history: List[PGI_State] = []
        
    def PGI_compute(self, system_state: Dict) -> PGI_State:
        """
        Calculate current PGI from system state.
        
        Formal Definition:
            PGI(S, t) = f(S, t) where f maps system metrics to
            generativity components
        
        Addendum v1.2 Section: PGI.2.2
        
        Args:
            system_state: Dictionary with system metrics
            
        Returns:
            PGI_State with computed components
        """
        import time
        
        # Extract or compute components
        G_rate = system_state.get('transformations_per_time', 0.0)
        CO = system_state.get('constraint_openness', 0.5)
        S_div = system_state.get('substrate_diversity', 0.5)
        Conn = system_state.get('connectivity', 0.5)
        Adopt = system_state.get('adoption_rate', 0.5)
        Res = system_state.get('resilience', 0.5)
        
        # If not provided, estimate from available data
        if 'coherence_scores' in system_state:
            C = np.array(system_state['coherence_scores'])
            CO = np.mean(C)  # Constraint openness proxy
            S_div = np.std(C)  # Diversity proxy
            Conn = 1.0 - np.mean(np.abs(np.diff(C)))  # Smoothness as connectivity
        
        pgi_state = PGI_State(
            G_rate=G_rate,
            CO=CO,
            S_div=S_div,
            Conn=Conn,
            Adopt=Adopt,
            Res=Res,
            timestamp=system_state.get('timestamp', time.time())
        )
        
        self.history.append(pgi_state)
        return pgi_state
    
    def PGI_delta(self, state_t: PGI_State, state_t1: PGI_State) -> float:
        """
        Compute ΔG_t between two states.
        
        Formal Definition:
            ΔG_t = PGI(S, t+1) - PGI(S, t)
        
        Addendum v1.2 Section: PGI.2.3
        
        Args:
            state_t: Earlier state
            state_t1: Later state
            
        Returns:
            Change in generativity
        """
        return state_t1.total_pgi() - state_t.total_pgi()
    
    def PGI_verify_conservation(self) -> Tuple[bool, List[float]]:
        """
        Verify conservation law: dXGI/dt ≥ 0.
        
        Checks that PGI is non-decreasing over time.
        
        Formal Definition:
            ∀ t: d(PGI_total)/dt ≥ 0
            (generative capacity must not decrease)
        
        Addendum v1.2 Section: PGI.3.1
        
        Returns:
            (is_conserved, deltas)
        """
        if len(self.history) < 2:
            return True, []
        
        deltas = []
        for i in range(1, len(self.history)):
            delta = self.PGI_delta(self.history[i-1], self.history[i])
            deltas.append(delta)
        
        # Conservation holds if all deltas >= 0 (or mostly >= 0 with small violations)
        violations = sum(1 for d in deltas if d < -1e-6)
        is_conserved = violations == 0
        
        return is_conserved, deltas
    
    def PGI_track_evolution(self) -> Dict[str, List[float]]:
        """
        Extract time series of PGI components.
        
        Addendum v1.2 Section: PGI.3.2
        
        Returns:
            Dictionary mapping component names to time series
        """
        evolution = {
            'G_rate': [],
            'CO': [],
            'S_div': [],
            'Conn': [],
            'Adopt': [],
            'Res': [],
            'total': [],
            'timestamp': []
        }
        
        for state in self.history:
            evolution['G_rate'].append(state.G_rate)
            evolution['CO'].append(state.CO)
            evolution['S_div'].append(state.S_div)
            evolution['Conn'].append(state.Conn)
            evolution['Adopt'].append(state.Adopt)
            evolution['Res'].append(state.Res)
            evolution['total'].append(state.total_pgi())
            evolution['timestamp'].append(state.timestamp)
        
        return evolution


# =============================================================================
# v1.2 Complexity Metrics
# =============================================================================

def PGI_compression_ratio(data: np.ndarray) -> float:
    """
    Kolmogorov complexity proxy via compression.
    
    Lower compression ratio → higher complexity.
    
    Formal Definition:
        K(x) ≈ |compressed(x)| / |x|
        where smaller ratio indicates less compressible (more complex) data
    
    Addendum v1.2 Section: PGI.4.1
    
    Args:
        data: Numpy array to analyze
        
    Returns:
        Compression ratio [0, 1]
    """
    # Convert to bytes
    data_bytes = data.tobytes()
    
    # Compress
    compressed = zlib.compress(data_bytes)
    
    # Ratio
    ratio = len(compressed) / len(data_bytes)
    
    return ratio


def PGI_entropy_estimate(distribution: np.ndarray) -> float:
    """
    Shannon entropy as generativity proxy.
    
    Higher entropy → higher generative potential.
    
    Formal Definition:
        H(X) = -Σ p(x) log₂ p(x)
    
    Addendum v1.2 Section: PGI.4.2
    
    Args:
        distribution: Probability distribution (must sum to 1)
        
    Returns:
        Shannon entropy in bits
    """
    # Normalize to ensure valid distribution
    dist = np.array(distribution)
    dist = dist / np.sum(dist)
    
    # Remove zeros to avoid log(0)
    dist = dist[dist > 0]
    
    # Compute entropy
    entropy = -np.sum(dist * np.log2(dist))
    
    return entropy


def PGI_complexity_delta(data_t: np.ndarray, data_t1: np.ndarray) -> float:
    """
    Measure complexity change between states.
    
    Combines compression ratio and entropy.
    
    Addendum v1.2 Section: PGI.4.3
    
    Args:
        data_t: Earlier state data
        data_t1: Later state data
        
    Returns:
        Complexity change (positive = increasing complexity)
    """
    # Compression-based complexity
    comp_t = 1.0 - PGI_compression_ratio(data_t)  # Invert: higher = more complex
    comp_t1 = 1.0 - PGI_compression_ratio(data_t1)
    
    # Entropy-based complexity (if data can be interpreted as distribution)
    try:
        ent_t = PGI_entropy_estimate(data_t)
        ent_t1 = PGI_entropy_estimate(data_t1)
        
        # Weighted combination
        delta = 0.5 * (comp_t1 - comp_t) + 0.5 * (ent_t1 - ent_t)
    except:
        # Fallback to compression only
        delta = comp_t1 - comp_t
    
    return delta


# =============================================================================
# v1.2 Example Usage
# =============================================================================

if __name__ == "__main__":
    print("PGI (Phenomenological Generativity Index) v1.2 - Test")
    print("=" * 60)
    
    # Initialize tracker
    tracker = PGI_Tracker()
    
    # Simulate system evolution
    np.random.seed(42)
    print("\nSimulating system evolution:")
    
    for t in range(5):
        # Create synthetic system state
        C = np.random.rand(3) * 0.5 + 0.5  # Coherence scores improving
        state = {
            'coherence_scores': C,
            'transformations_per_time': t * 0.1,
            'timestamp': t
        }
        
        pgi = tracker.PGI_compute(state)
        print(f"t={t}: PGI={pgi.total_pgi():.4f}, G_rate={pgi.G_rate:.3f}, CO={pgi.CO:.3f}")
    
    # Verify conservation
    is_conserved, deltas = tracker.PGI_verify_conservation()
    print(f"\nConservation Law (dPGI/dt ≥ 0): {'✓ PASS' if is_conserved else '✗ FAIL'}")
    print(f"ΔG_t values: {[f'{d:.4f}' for d in deltas]}")
    
    # Test complexity metrics
    print("\nComplexity metrics:")
    data1 = np.random.rand(100)
    data2 = np.random.rand(100) + np.sin(np.linspace(0, 4*np.pi, 100))  # More structured
    
    comp1 = PGI_compression_ratio(data1)
    comp2 = PGI_compression_ratio(data2)
    print(f"Compression ratio - Random: {comp1:.3f}, Structured: {comp2:.3f}")
    
    # Entropy
    dist1 = np.ones(10) / 10  # Uniform
    dist2 = np.array([0.5, 0.3, 0.1, 0.05, 0.03, 0.02, 0.0, 0.0, 0.0, 0.0])  # Skewed
    
    ent1 = PGI_entropy_estimate(dist1)
    ent2 = PGI_entropy_estimate(dist2)
    print(f"Entropy - Uniform: {ent1:.3f} bits, Skewed: {ent2:.3f} bits")
    
    # Complexity delta
    delta_comp = PGI_complexity_delta(data1, data2)
    print(f"Complexity change: {delta_comp:.4f}")
    
    # Track evolution
    evolution = tracker.PGI_track_evolution()
    print(f"\nPGI evolution over {len(evolution['total'])} timesteps:")
    print(f"Initial PGI: {evolution['total'][0]:.4f}")
    print(f"Final PGI: {evolution['total'][-1]:.4f}")
    print(f"Net change: {evolution['total'][-1] - evolution['total'][0]:.4f}")
    
    print("\n" + "=" * 60)
    print("PGI test complete.")
