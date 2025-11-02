# Architecture v1.2: Stratified Design Documentation

**Version:** v1.2.0-α-non-destructive  
**Status:** Enhancement Layer (Non-Destructive)  
**Date:** November 2025  
**Framework:** Addendum v1.2 Compliance

---

## Overview

This document outlines the stratified architecture introduced in **Addendum v1.2**, which enhances the Generativity Theory with three core subsystems while maintaining full backward compatibility with v1.1.

The v1.2 architecture is **non-destructive**: all legacy constructs (Λ-substrate, modal registers, etc.) are preserved and cross-referenced with their new formal equivalents.

---

## Three-System Architecture

### 1. LPL (Logical Presupposition Lattice)

**Purpose:** Express dependency graphs among conditions, axioms, and logical presuppositions.

**Key Components:**
- Dependency graph representation of the 79 CFPE conditions
- DAG (Directed Acyclic Graph) condensation for cycle detection
- SCC (Strongly Connected Component) analysis
- Proof-theoretic tracing utilities
- Integration with Lean4 formal proofs

**Formal Definition:**
```
LPL := ⟨V, E, ⊑⟩
  where:
    V = {C₁, C₂, ..., C₇₉} ∪ {Axioms} ∪ {Theorems}
    E ⊆ V × V (presupposition edges)
    ⊑ is a partial order on V (logical dependency ordering)
```

**Implementation Functions:**
- `LPL_build_graph()`: Construct dependency graph
- `LPL_find_presuppositions(condition)`: Return all logical prerequisites
- `LPL_check_circular_dependency()`: Detect circular reasoning
- `LPL_topological_sort()`: Order conditions by dependency level
- `LPL_minimal_basis()`: Find minimal axiom set for a theorem

**Mapping to Legacy:**
- Λ-substrate dependencies → LPL edge relations
- CFPE hierarchy → LPL topological levels
- Performative contradiction tests → LPL consistency checks

---

### 2. PCM (Paraconsistent Contradiction Metabolism)

**Purpose:** Formalize the metabolic processing of contradictions through rewrite rules.

**Key Components:**
- Rewrite rule operator σ: (φ ∧ ¬φ) ↦ G^ω
- Safe-contradiction handling: (φ ∧ ¬φ) ⊬ ψ (no explosion)
- Convergence guarantee: metabolic rate λ < 1
- SAT (Structured Anomaly Token) processing pipeline
- Bloom/Scar operators with formal convergence proofs

**Formal Definition:**
```
PCM := ⟨Ω₀, σ, Γ, λ⟩
  where:
    Ω₀: Zero-Degree Operator (φ ∧ ¬φ) → G^ω
    σ: Rewrite rule set {σ₁, σ₂, ..., σₙ}
    Γ: Generativity function (monotonically increasing)
    λ: Metabolic convergence rate (λ < 1)
```

**Convergence Condition:**
```
∀ SAT s: ||s_{t+1}|| ≤ λ·||s_t|| + ε
where λ < 1 ensures convergence
```

**Implementation Functions:**
- `PCM_metabolize(contradiction)`: Apply Ω₀ operator
- `PCM_apply_rewrite(sat, rule)`: Execute rewrite rule σ
- `PCM_check_convergence(history)`: Verify λ < 1
- `PCM_safe_contradiction(phi, not_phi)`: Handle without explosion
- `PCM_generate_bloom(severe_sat)`: Trigger architectural expansion

**Mapping to Legacy:**
- Ω₀ operator → PCM_metabolize
- Metabolic Cycle → PCM pipeline
- Scar formation → PCM history tracking
- Bloom trigger → PCM_generate_bloom

---

### 3. PGI (Phenomenological Generativity Index)

**Purpose:** Quantify generative capacity and complexity evolution.

**Key Components:**
- Complexity-change measurement: ΔG_t
- Compression-based metrics
- Entropy proxies for generativity
- Temporal evolution tracking
- Multi-dimensional generativity scoring

**Formal Definition:**
```
PGI(S, t) := ⟨G_rate, CO, S_div, Conn, Adopt, Res⟩
  where:
    G_rate: Novel transformations per time unit
    CO: Constraint openness (0-1 scale)
    S_div: Substrate diversity
    Conn: Network connectivity
    Adopt: Adoption rate of new structures
    Res: Resilience to perturbation
```

**Generativity Change:**
```
ΔG_t = PGI(S, t+1) - PGI(S, t)
Conservation Law: dXGI_total/dt ≥ 0
```

**Implementation Functions:**
- `PGI_compute(system_state)`: Calculate current generativity
- `PGI_delta(state_t, state_t1)`: Compute ΔG_t
- `PGI_compression_ratio(data)`: Kolmogorov complexity proxy
- `PGI_entropy_estimate(distribution)`: Shannon entropy
- `PGI_track_evolution(history)`: Plot generativity trajectory
- `PGI_verify_conservation()`: Check dXGI/dt ≥ 0

**Mapping to Legacy:**
- XGI (Xenogenerative Index) → PGI primary metric
- Generativity conservation → PGI_verify_conservation
- Complexity metrics → PGI compression/entropy functions

---

## Naming Conventions (v1.2)

All new functions and classes follow these prefixes:

- **LPL_*** → Logical Presupposition Lattice utilities
- **PCM_*** → Paraconsistent Contradiction Metabolism operators  
- **PGI_*** → Phenomenological Generativity Index metrics

Legacy functions are marked with:
```python
# LEGACY: retained for historical context
# v1.2 equivalent: LPL_build_graph()
def build_dependency_graph():
    ...
```

---

## Backward Compatibility

**Principle:** All v1.1 code continues to work unchanged.

**Strategy:**
1. Legacy functions preserved with deprecation notices
2. New v1.2 functions implemented alongside legacy
3. Wrapper functions bridge legacy calls to v1.2 implementations
4. Documentation cross-references old and new equivalents

**Example:**
```python
# LEGACY: Ω₀ operator (v1.1)
# v1.2 equivalent: PCM_metabolize()
def omega_zero_operator(contradiction):
    """Original v1.1 implementation."""
    return metabolize_contradiction(contradiction)

# v1.2: New formal implementation
def PCM_metabolize(contradiction: Contradiction) -> GenerativeState:
    """
    Paraconsistent Contradiction Metabolism operator.
    Maps (φ ∧ ¬φ) → G^ω via rewrite rules.
    
    Addendum v1.2 Section: PCM.2.1
    """
    return omega_zero_operator(contradiction)  # delegates to legacy
```

---

## Integration with Formal Systems

### Lean4 Integration (Planned)

```lean4
-- LPL: Dependency graph structure
structure LPL where
  vertices : Finset Condition
  edges : Finset (Condition × Condition)
  is_dag : IsDAG edges
  
-- PCM: Metabolic rewrite system
def PCM_metabolize (φ : Prop) (h : φ ∧ ¬φ) : GenerativeState := ...

-- PGI: Generativity measurement
def PGI_compute (s : SystemState) : ℝ := ...
```

### Python Type Annotations

```python
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass

@dataclass
class Condition:
    """CFPE condition with v1.2 metadata."""
    id: str  # e.g., "C1", "C13"
    category: str  # e.g., "Ontological", "Logical-Formal"
    dependencies: Set[str]  # LPL edges
    
@dataclass  
class SAT:
    """Structured Anomaly Token (v1.2 formalization)."""
    contradiction: Tuple[str, str]  # (φ, ¬φ)
    severity: float  # [0, 1]
    rewrite_rules: List[str]  # Applicable PCM rules
```

---

## Documentation Standards (v1.2)

Every function must include:

1. **Version header:** `# v1.2-Refactor: ...`
2. **Docstring:** Plain English description
3. **Formal definition:** Mathematical notation
4. **Addendum reference:** Section number
5. **Legacy mapping:** If replacing v1.1 code

**Template:**
```python
# v1.2-Refactor: aligned with Addendum v1.2 (Non-Destructive Update)

def PCM_apply_rewrite(sat: SAT, rule: str) -> GenerativeState:
    """
    Apply a paraconsistent rewrite rule to a contradiction.
    
    Formal Definition:
        σ: (φ ∧ ¬φ) ↦ G^ω
        where σ ∈ RewriteRules
        
    Addendum v1.2 Section: PCM.3.2
    
    Legacy Equivalent: apply_metabolic_transformation() from v1.1
    
    Args:
        sat: Structured Anomaly Token containing contradiction
        rule: Identifier of rewrite rule to apply
        
    Returns:
        GenerativeState after metabolic processing
    """
    pass
```

---

## Staged Migration Path

**Phase 1 (Current):** Annotation & Documentation
- Add v1.2 headers to all files
- Document LPL/PCM/PGI architecture
- Mark legacy code with cross-references

**Phase 2:** Implementation
- Implement LPL utility functions
- Formalize PCM operators
- Add PGI metrics

**Phase 3:** Testing & Validation
- Unit tests for each subsystem
- Integration tests for LPL↔PCM↔PGI interactions
- Convergence proofs for PCM

**Phase 4:** Lean4 Mechanization
- Port LPL to Lean4
- Prove PCM convergence formally
- Verify PGI conservation law

---

## Version History

- **v1.0** (September 2025): Initial framework
- **v1.1** (November 1, 2025): Metabolic addendum (6 contradictions resolved)
- **v1.2** (November 2, 2025): Stratified architecture (LPL/PCM/PGI)

---

## References

- **Addendum v1.1:** `Addendum and Errata /Addendum v1.1.md`
- **CFPE Conditions:** `The Universal Conditions/`
- **Principia Generativarum:** Main theoretical document
- **Tools:** `/tools/` (Python implementations)

---

**Document Status:** ✓ Complete  
**Next Update:** Integration with Lean4 formal proofs

Q.E.D.
