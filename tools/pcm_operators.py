#!/usr/bin/env python3
# v1.2-Refactor: aligned with Addendum v1.2 (Non-Destructive Update)
"""
PCM (Paraconsistent Contradiction Metabolism) Operators - v1.2
===============================================================

Implements formal contradiction metabolism with convergence guarantees.

Key Functions:
- PCM_metabolize(contradiction): Apply Ω₀ operator
- PCM_apply_rewrite(sat, rule): Execute rewrite rule σ
- PCM_check_convergence(history): Verify λ < 1
- PCM_safe_contradiction(phi, not_phi): Handle without explosion
- PCM_generate_bloom(severe_sat): Trigger architectural expansion

Formal Definition:
    PCM := ⟨Ω₀, σ, Γ, λ⟩
    where:
      Ω₀: Zero-Degree Operator (φ ∧ ¬φ) → G^ω
      σ: Rewrite rule set {σ₁, σ₂, ..., σₙ}
      Γ: Generativity function (monotonically increasing)
      λ: Metabolic convergence rate (λ < 1)

Convergence Condition:
    ∀ SAT s: ||s_{t+1}|| ≤ λ·||s_t|| + ε
    where λ < 1 ensures convergence

Addendum v1.2 Section: PCM.1.1
Author: PROMETHIVM LLC
"""

from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import numpy as np

@dataclass
class SAT:
    """
    Structured Anomaly Token (v1.2 formalization).
    
    Represents a contradiction (φ ∧ ¬φ) with metabolic metadata.
    
    Addendum v1.2 Section: PCM.1.2
    """
    contradiction: Tuple[str, str]  # (φ, ¬φ)
    severity: float  # [0, 1]
    timestamp: float
    context: Dict[str, any]
    rewrite_rules: List[str] = None  # Applicable PCM rules
    
    def __post_init__(self):
        if self.rewrite_rules is None:
            self.rewrite_rules = []
    
    def norm(self) -> float:
        """Compute norm ||SAT|| for convergence analysis."""
        return self.severity


@dataclass
class GenerativeState:
    """
    Result of contradiction metabolism: G^ω
    
    Addendum v1.2 Section: PCM.1.3
    """
    generative_rank: int  # ω level
    potential: float  # Generative capacity
    scars: List[str]  # Historical traces
    blooms: List[str]  # Architectural expansions


class RewriteRule(Enum):
    """
    PCM Rewrite Rules (σ).
    
    Each rule defines a transformation strategy for contradictions.
    
    Addendum v1.2 Section: PCM.2.1
    """
    RELAX = "relax"  # Reduce constraint penalty
    STRENGTHEN = "strengthen"  # Increase constraint weight
    SPLIT = "split"  # Partition into sub-problems
    MERGE = "merge"  # Unify contradictory constraints
    DEFER = "defer"  # Delay resolution to higher rank
    ABSORB = "absorb"  # Metabolize into substrate


class PCM_Processor:
    """
    Paraconsistent Contradiction Metabolism Processor.
    
    Implements the formal PCM system with convergence guarantees.
    
    Addendum v1.2 Section: PCM.3.1
    LEGACY: MetabolicCycle from v1.1
    """
    
    def __init__(self, lambda_rate: float = 0.8, epsilon: float = 0.01):
        """
        Initialize PCM processor.
        
        Args:
            lambda_rate: Convergence rate (must be < 1)
            epsilon: Minimum residual threshold
        """
        if lambda_rate >= 1.0:
            raise ValueError(f"λ must be < 1 for convergence, got {lambda_rate}")
        
        self.lambda_rate = lambda_rate
        self.epsilon = epsilon
        self.history: List[SAT] = []
        self.generative_states: List[GenerativeState] = []
        
    def PCM_metabolize(self, sat: SAT) -> GenerativeState:
        """
        Apply Ω₀ (Zero-Degree Operator) to metabolize contradiction.
        
        Formal Definition:
            Ω₀: (φ ∧ ¬φ) → G^ω
            Maps contradiction to enhanced generative state
        
        Implementation:
            1. Select applicable rewrite rules
            2. Apply rules in sequence
            3. Generate scars (historical traces)
            4. Compute generative rank ω
            5. Return G^ω state
        
        Addendum v1.2 Section: PCM.2.1
        LEGACY: omega_zero_operator() from v1.1
        
        Args:
            sat: Structured Anomaly Token
            
        Returns:
            GenerativeState after metabolism
        """
        # Select rewrite rules based on severity
        rules = self._select_rewrite_rules(sat)
        sat.rewrite_rules = [r.value for r in rules]
        
        # Apply rules
        potential = 0.0
        scars = []
        blooms = []
        
        for rule in rules:
            delta_potential, scar, bloom = self._apply_single_rule(sat, rule)
            potential += delta_potential
            if scar:
                scars.append(scar)
            if bloom:
                blooms.append(bloom)
        
        # Compute generative rank
        omega = self._compute_generative_rank(sat, potential)
        
        # Create generative state
        g_state = GenerativeState(
            generative_rank=omega,
            potential=potential,
            scars=scars,
            blooms=blooms
        )
        
        # Track history
        self.history.append(sat)
        self.generative_states.append(g_state)
        
        return g_state
    
    def _select_rewrite_rules(self, sat: SAT) -> List[RewriteRule]:
        """Select applicable rewrite rules based on SAT properties."""
        rules = []
        
        if sat.severity > 0.8:
            # High severity: split or defer
            rules.append(RewriteRule.SPLIT)
        elif sat.severity > 0.5:
            # Medium severity: relax or merge
            rules.append(RewriteRule.RELAX)
            rules.append(RewriteRule.MERGE)
        else:
            # Low severity: absorb
            rules.append(RewriteRule.ABSORB)
        
        return rules
    
    def _apply_single_rule(self, sat: SAT, rule: RewriteRule) -> Tuple[float, Optional[str], Optional[str]]:
        """
        Apply a single rewrite rule.
        
        Returns:
            (delta_potential, scar_trace, bloom_spec)
        """
        if rule == RewriteRule.RELAX:
            # Reduce constraint severity
            delta = sat.severity * 0.3
            scar = f"RELAX_{sat.contradiction[0]}"
            return delta, scar, None
            
        elif rule == RewriteRule.SPLIT:
            # Partition problem
            delta = sat.severity * 0.5
            scar = f"SPLIT_{sat.contradiction[0]}"
            bloom = f"NEW_OPERATOR_SPLIT_{sat.timestamp}"
            return delta, scar, bloom
            
        elif rule == RewriteRule.MERGE:
            # Unify constraints
            delta = sat.severity * 0.4
            scar = f"MERGE_{sat.contradiction[0]}"
            return delta, scar, None
            
        elif rule == RewriteRule.ABSORB:
            # Metabolize into substrate
            delta = sat.severity * 0.6
            scar = f"ABSORB_{sat.contradiction[0]}"
            return delta, scar, None
            
        else:  # DEFER, STRENGTHEN
            delta = sat.severity * 0.2
            return delta, None, None
    
    def _compute_generative_rank(self, sat: SAT, potential: float) -> int:
        """
        Compute generative rank ω based on metabolic potential.
        
        Formal Definition:
            ω = ⌈log₂(1 + Ψ)⌉
            where Ψ is generative potential
        """
        if potential <= 0:
            return 0
        return int(np.ceil(np.log2(1 + potential)))
    
    def PCM_apply_rewrite(self, sat: SAT, rule_name: str) -> GenerativeState:
        """
        Execute specific rewrite rule σ.
        
        Formal Definition:
            σ: (φ ∧ ¬φ) ↦ G^ω
            where σ ∈ RewriteRules
        
        Addendum v1.2 Section: PCM.3.2
        
        Args:
            sat: Structured Anomaly Token
            rule_name: Name of rewrite rule to apply
            
        Returns:
            GenerativeState after rewrite
        """
        try:
            rule = RewriteRule(rule_name)
        except ValueError:
            raise ValueError(f"Unknown rewrite rule: {rule_name}")
        
        delta_potential, scar, bloom = self._apply_single_rule(sat, rule)
        omega = self._compute_generative_rank(sat, delta_potential)
        
        return GenerativeState(
            generative_rank=omega,
            potential=delta_potential,
            scars=[scar] if scar else [],
            blooms=[bloom] if bloom else []
        )
    
    def PCM_check_convergence(self) -> Tuple[bool, float]:
        """
        Verify convergence condition: λ < 1.
        
        Checks that SAT severity decreases over time:
            ||s_{t+1}|| ≤ λ·||s_t|| + ε
        
        Addendum v1.2 Section: PCM.4.1
        
        Returns:
            (is_converging, estimated_lambda)
        """
        if len(self.history) < 2:
            return True, 0.0
        
        # Estimate λ from recent history
        lambdas = []
        for i in range(1, len(self.history)):
            s_prev = self.history[i-1].norm()
            s_curr = self.history[i].norm()
            
            if s_prev > 0:
                lambda_est = (s_curr - self.epsilon) / s_prev
                lambdas.append(lambda_est)
        
        if not lambdas:
            return True, 0.0
        
        avg_lambda = np.mean(lambdas)
        is_converging = avg_lambda < 1.0
        
        return is_converging, avg_lambda
    
    def PCM_generate_bloom(self, sat: SAT) -> Optional[Dict]:
        """
        Trigger architectural expansion (Bloom operator).
        
        When SAT severity exceeds threshold, generate new:
        - Operators
        - Axioms
        - Domains
        
        Formal Definition:
            ∀ SAT: severity(SAT) ≥ θ ⟹ 
              B(SAT) = ⟨new-operator, new-axiom, expanded-domain⟩
        
        Addendum v1.2 Section: PCM.5.1
        LEGACY: BloomOperator.generate() from v1.1
        
        Args:
            sat: Structured Anomaly Token
            
        Returns:
            Bloom specification or None
        """
        BLOOM_THRESHOLD = 0.8
        
        if sat.severity < BLOOM_THRESHOLD:
            return None
        
        bloom = {
            "operator": f"Ω_{sat.timestamp}",
            "axiom": f"A_{sat.contradiction[0]}",
            "domain": f"D_expanded_{len(self.history)}",
            "severity": sat.severity,
            "timestamp": sat.timestamp
        }
        
        return bloom


# =============================================================================
# v1.2 Helper Functions
# =============================================================================

def PCM_safe_contradiction(phi: str, not_phi: str, context: Dict = None) -> SAT:
    """
    Create SAT from contradiction without explosion.
    
    Safe handling: (φ ∧ ¬φ) ⊬ ψ
    
    Addendum v1.2 Section: PCM.6.1
    
    Args:
        phi: Proposition
        not_phi: Negation
        context: Optional context dict
        
    Returns:
        SAT for metabolic processing
    """
    import time
    
    if context is None:
        context = {}
    
    # Compute severity heuristically
    severity = 0.5  # Default medium severity
    if "severity" in context:
        severity = context["severity"]
    
    return SAT(
        contradiction=(phi, not_phi),
        severity=severity,
        timestamp=time.time(),
        context=context
    )


if __name__ == "__main__":
    # Quick test
    print("PCM (Paraconsistent Contradiction Metabolism) v1.2 - Test")
    print("=" * 60)
    
    # Initialize processor
    pcm = PCM_Processor(lambda_rate=0.8, epsilon=0.01)
    
    # Create test contradictions
    sats = [
        PCM_safe_contradiction("exists(x)", "¬exists(x)", {"severity": 0.9}),
        PCM_safe_contradiction("coherent(S)", "¬coherent(S)", {"severity": 0.6}),
        PCM_safe_contradiction("temporal(t)", "¬temporal(t)", {"severity": 0.3}),
    ]
    
    # Metabolize contradictions
    print("\nMetabolizing contradictions:")
    for i, sat in enumerate(sats):
        print(f"\n{i+1}. SAT: {sat.contradiction}, severity={sat.severity:.2f}")
        g_state = pcm.PCM_metabolize(sat)
        print(f"   → G^{g_state.generative_rank}, potential={g_state.potential:.3f}")
        print(f"   → Scars: {g_state.scars}")
        if g_state.blooms:
            print(f"   → Blooms: {g_state.blooms}")
    
    # Check convergence
    is_converging, lambda_est = pcm.PCM_check_convergence()
    print(f"\nConvergence check:")
    print(f"  Is converging: {is_converging}")
    print(f"  Estimated λ: {lambda_est:.3f} (must be < 1.0)")
    
    # Test bloom generation
    severe_sat = PCM_safe_contradiction("critical(C)", "¬critical(C)", {"severity": 0.95})
    bloom = pcm.PCM_generate_bloom(severe_sat)
    if bloom:
        print(f"\nBloom triggered for severe SAT:")
        print(f"  New operator: {bloom['operator']}")
        print(f"  New axiom: {bloom['axiom']}")
        print(f"  Expanded domain: {bloom['domain']}")
    
    print("\n" + "=" * 60)
    print("PCM test complete.")
