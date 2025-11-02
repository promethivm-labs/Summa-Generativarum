#!/usr/bin/env python3
# v1.2-Refactor: aligned with Addendum v1.2 (Non-Destructive Update)
"""
LPL (Logical Presupposition Lattice) Utilities - v1.2
======================================================

Implements dependency graph analysis for the 79 CFPE conditions.

Key Functions:
- LPL_build_graph(): Construct dependency graph from conditions
- LPL_find_presuppositions(condition): Return all logical prerequisites
- LPL_check_circular_dependency(): Detect circular reasoning
- LPL_topological_sort(): Order conditions by dependency level
- LPL_minimal_basis(): Find minimal axiom set for a theorem

Formal Definition:
    LPL := ⟨V, E, ⊑⟩
    where:
      V = {C₁, C₂, ..., C₇₉} ∪ {Axioms} ∪ {Theorems}
      E ⊆ V × V (presupposition edges)
      ⊑ is a partial order on V (logical dependency ordering)

Addendum v1.2 Section: LPL.1.1
Author: PROMETHIVM LLC
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass
class Condition:
    """
    CFPE condition with v1.2 metadata.
    
    Addendum v1.2 Section: LPL.1.2
    """
    id: str  # e.g., "C1", "C13"
    category: str  # e.g., "Ontological", "Logical-Formal"
    name: str
    dependencies: Set[str]  # LPL edges: conditions this one presupposes
    tier: int  # Hierarchical level (0 = foundational)


class LPL_Graph:
    """
    Logical Presupposition Lattice - Dependency Graph Structure.
    
    Represents the partial ordering of CFPE conditions based on logical
    presupposition relationships.
    
    Addendum v1.2 Section: LPL.2.1
    """
    
    def __init__(self):
        """Initialize empty LPL graph."""
        self.vertices: Dict[str, Condition] = {}
        self.edges: Dict[str, Set[str]] = defaultdict(set)  # condition_id -> dependencies
        self.reverse_edges: Dict[str, Set[str]] = defaultdict(set)  # condition_id -> dependents
        
    def add_condition(self, condition: Condition):
        """
        Add a condition to the LPL graph.
        
        Addendum v1.2 Section: LPL.2.2
        
        Args:
            condition: CFPE condition with dependencies
        """
        self.vertices[condition.id] = condition
        for dep in condition.dependencies:
            self.edges[condition.id].add(dep)
            self.reverse_edges[dep].add(condition.id)
            
    def LPL_find_presuppositions(self, condition_id: str) -> Set[str]:
        """
        Find all logical prerequisites (transitive closure).
        
        Returns all conditions that must hold for the given condition
        to be satisfied.
        
        Formal Definition:
            Presup(C) = {D ∈ V | D ⊑ C}
            (transitive closure of ⊑ relation)
        
        Addendum v1.2 Section: LPL.3.1
        
        Args:
            condition_id: ID of condition to analyze
            
        Returns:
            Set of all prerequisite condition IDs
        """
        visited = set()
        queue = deque([condition_id])
        
        while queue:
            current = queue.popleft()
            if current in visited or current not in self.edges:
                continue
            visited.add(current)
            
            for dep in self.edges[current]:
                if dep not in visited:
                    queue.append(dep)
                    
        visited.discard(condition_id)  # Don't include self
        return visited
    
    def LPL_check_circular_dependency(self) -> Optional[List[str]]:
        """
        Detect circular dependencies (cycles in presupposition graph).
        
        Uses Tarjan's algorithm for strongly connected components.
        
        Formal Definition:
            Valid LPL must be a DAG (Directed Acyclic Graph)
            Circular dependency exists if ∃ C₁, ..., Cₙ:
              C₁ ⊑ C₂ ⊑ ... ⊑ Cₙ ⊑ C₁
        
        Addendum v1.2 Section: LPL.3.2
        
        Returns:
            None if acyclic, list of cycle nodes if circular
        """
        # Simple DFS-based cycle detection
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in self.vertices}
        
        def dfs(node, path):
            if color[node] == GRAY:
                # Found cycle
                cycle_start = path.index(node)
                return path[cycle_start:]
            if color[node] == BLACK:
                return None
                
            color[node] = GRAY
            path.append(node)
            
            for neighbor in self.edges.get(node, []):
                if neighbor in self.vertices:
                    result = dfs(neighbor, path[:])
                    if result:
                        return result
                        
            color[node] = BLACK
            return None
        
        for vertex in self.vertices:
            if color[vertex] == WHITE:
                cycle = dfs(vertex, [])
                if cycle:
                    return cycle
        return None
    
    def LPL_topological_sort(self) -> List[str]:
        """
        Order conditions by dependency level (topological sort).
        
        Returns conditions in order such that dependencies come before
        dependents.
        
        Formal Definition:
            TopSort(LPL) = sequence (C₁, ..., C₇₉) where
              ∀ i < j: Cⱼ ⊑ Cᵢ implies i < j
              (no dependency can come after its dependent)
        
        Addendum v1.2 Section: LPL.3.3
        
        Returns:
            List of condition IDs in dependency order
        """
        # Kahn's algorithm
        in_degree = {v: 0 for v in self.vertices}
        for node in self.vertices:
            for dep in self.edges.get(node, []):
                if dep in in_degree:
                    in_degree[node] += 1
        
        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for dependent in self.reverse_edges.get(node, []):
                if dependent in in_degree:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        if len(result) != len(self.vertices):
            raise ValueError("Graph contains cycle - cannot topologically sort")
            
        return result
    
    def LPL_minimal_basis(self, target_condition: str) -> Set[str]:
        """
        Find minimal set of axioms needed to derive a condition.
        
        Returns the smallest set of foundational conditions that
        logically entail the target condition.
        
        Formal Definition:
            MinBasis(C) = {A ∈ Axioms | A ⊑ C ∧ 
                          ∄ A' ⊂ A: A' ⊑ C}
            (minimal set of axioms that imply C)
        
        Addendum v1.2 Section: LPL.3.4
        
        Args:
            target_condition: ID of condition to analyze
            
        Returns:
            Set of minimal prerequisite axiom IDs
        """
        all_presups = self.LPL_find_presuppositions(target_condition)
        
        # Find foundational conditions (tier 0 or no dependencies)
        minimal = set()
        for presup in all_presups:
            if presup in self.vertices:
                cond = self.vertices[presup]
                if cond.tier == 0 or not self.edges.get(presup):
                    minimal.add(presup)
        
        return minimal


# =============================================================================
# v1.2 Helper Functions
# =============================================================================

def LPL_build_graph(conditions: List[Condition]) -> LPL_Graph:
    """
    Construct LPL dependency graph from CFPE conditions.
    
    Addendum v1.2 Section: LPL.4.1
    LEGACY: build_dependency_graph() from v1.1
    
    Args:
        conditions: List of CFPE conditions with dependency metadata
        
    Returns:
        LPL_Graph instance
    """
    graph = LPL_Graph()
    for condition in conditions:
        graph.add_condition(condition)
    return graph


def LPL_validate_graph(graph: LPL_Graph) -> Tuple[bool, Optional[str]]:
    """
    Validate LPL graph structure.
    
    Checks:
    - No circular dependencies
    - All referenced dependencies exist
    - Graph is a valid DAG
    
    Addendum v1.2 Section: LPL.4.2
    
    Returns:
        (is_valid, error_message)
    """
    # Check for cycles
    cycle = graph.LPL_check_circular_dependency()
    if cycle:
        return False, f"Circular dependency detected: {' -> '.join(cycle)}"
    
    # Check for dangling references
    for node_id, deps in graph.edges.items():
        for dep in deps:
            if dep not in graph.vertices:
                return False, f"Condition {node_id} references non-existent dependency {dep}"
    
    return True, None


# =============================================================================
# Example CFPE Conditions (v1.2 Schema)
# =============================================================================

def get_core_cfpe_conditions() -> List[Condition]:
    """
    Return core CFPE conditions with LPL dependencies.
    
    This is a minimal subset for demonstration. Full set would include all 79.
    
    Addendum v1.2 Section: LPL.5.1
    """
    return [
        # Ontological (C1-C10)
        Condition("C1", "Ontological", "Existence", set(), 0),
        Condition("C2", "Ontological", "Identity", {"C1"}, 1),
        Condition("C3", "Ontological", "Difference", {"C1", "C2"}, 1),
        
        # Logical-Formal (C11-C20)
        Condition("C11", "Logical-Formal", "Identity (Logical)", {"C2"}, 2),
        Condition("C12", "Logical-Formal", "Difference (Logical)", {"C3"}, 2),
        Condition("C13", "Logical-Formal", "Metabolic Non-Contradiction", {"C11", "C12"}, 3),
        
        # Temporal-Dynamical (C21-C30)
        Condition("C21", "Temporal-Dynamical", "Temporality", {"C1"}, 1),
        Condition("C22", "Temporal-Dynamical", "Causality", {"C21"}, 2),
        
        # Add more as needed...
    ]


if __name__ == "__main__":
    # Quick test
    print("LPL (Logical Presupposition Lattice) v1.2 - Test")
    print("=" * 60)
    
    conditions = get_core_cfpe_conditions()
    graph = LPL_build_graph(conditions)
    
    print(f"\nBuilt LPL graph with {len(graph.vertices)} conditions")
    
    # Validate
    is_valid, error = LPL_validate_graph(graph)
    print(f"Graph valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    
    # Topological sort
    try:
        sorted_ids = graph.LPL_topological_sort()
        print(f"\nTopological order: {sorted_ids}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Find presuppositions for C13
    if "C13" in graph.vertices:
        presups = graph.LPL_find_presuppositions("C13")
        print(f"\nPresuppositions for C13 (Metabolic Non-Contradiction): {presups}")
        
        minimal = graph.LPL_minimal_basis("C13")
        print(f"Minimal basis for C13: {minimal}")
    
    print("\n" + "=" * 60)
    print("LPL test complete.")
