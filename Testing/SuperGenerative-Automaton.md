# Supergenerative Automaton

## Short definition
A Supergenerative Automaton is an abstract machine that extends classical state machines by making transitions capable of producing structured outputs, spawning subordinate generators, and modifying generation rules at runtime. Informally, it combines the control discipline of an automaton with the creative, self-referential power of generative systems so that a single device can recognize inputs and construct arbitrarily nested artifacts (strings, trees, programs, signals) while possibly adapting during execution.

## Core idea (one line)
Combine stateful control (Q = set of possible machine states) with richer output actions and self‑modification so a single machine can generate multi-scale, hierarchical artifacts.

Formal translation: "Q is the set of all states the machine may be in."

## Formal ingredients (notation)
- Q — a finite or countable set of states (the possible states the machine can be in)  
    Translation: "Q denotes the set of possible control states of the automaton."

- $\Sigma_{in}$ — input alphabet (In formal terms: the set of all valid input symbols)  
    Translation: "Σ_in denotes the set of all input symbols the machine can read."

- $\Sigma_{out}$ — output alphabet (In formal terms: the set of all possible output elements)  
    Translation: "Σ_out denotes the set of tokens or output elements the machine may emit."

- $\varepsilon$ — the empty input symbol (In formal terms: a symbol representing null or no input)  
    Translation: "ε denotes the empty input (no symbol)."

- $\mathrm{Action}$ — a set of higher-order actions (In formal terms: the set of all valid operations)  
    Translation: "Action denotes the set of operations (emit, spawn, rewrite, etc.) that transitions may request."

- $q_0 \in Q$ — start state (In formal terms: the initial state element belonging to set Q)  
    Translation: "q₀ is the designated start state and is an element of Q."

- $\Sigma_{out}$ — output alphabet (tokens, tree constructors, program fragments).  
    Translation: "Restatement: Σ_out is the set of possible output tokens or constructors."

- $\varepsilon$ — the empty input symbol.  
    Translation: "Restatement: ε is the symbol representing no input."

- $\mathrm{Action}$ — a set of higher-order actions (see below).  
    Translation: "Restatement: Action is the set of executable action types."

- $q_0 \in Q$ — start state.  
    Translation: "Restatement: q₀ is the initial control state."

The transition relation is written as

$$\delta:\; Q \times (\Sigma_{in} \cup \{\varepsilon\}) \;\to\; \mathcal{P}(Q \times \mathrm{Action})$$

Translation: "The transition relation δ maps a current state and an input symbol (or ε) to a set (power set) of possible (next state, action) pairs."

where $\mathcal{P}(\cdot)$ denotes the power set. Intuitively, for a given current state and input symbol (or $\varepsilon$), $\delta$ returns a set of possible pairs $(q',a)$ where $q'$ is the next state and $a$ is an action to execute.

### Canonical Action types
- $\mathrm{emit}(s)$ — append $s \in \Sigma_{out}^*$ to the (global or local) output stream.  
    Translation: "emit(s) denotes appending the string s (a sequence over Σ_out) to the output."

- $\mathrm{spawn}(A)$ — start a subordinate generator $A$ (itself a supergenerative automaton or a generator closure) whose outputs will be interleaved or attached as a subtree.  
    Translation: "spawn(A) starts a new subordinate generator A whose output will be composed with the parent output."

- $\mathrm{rewrite}(r)$ — locally mutate the transition relation $\delta$ according to a rule $r$ (self‑modification).  
    Translation: "rewrite(r) modifies the machine's transition relation δ according to rule r."

- $\mathrm{choice}(\{(p_i,a_i)\})$ — probabilistic or weighted choice among actions $a_i$ with weights $p_i$.  
    Translation: "choice({(p_i,a_i)}) selects one action a_i with probability or weight p_i."

- $\mathrm{halt}$ — explicit stop action.  
    Translation: "halt denotes an explicit termination action."

Actions may be composed: for example, an action may both $\mathrm{emit}$ and $\mathrm{spawn}$. Implementations should define a deterministic execution semantics for composed actions.

## Configurations and runs (operational semantics)
A configuration is a tuple

$$C = (q, w, O, \mathcal{G}),$$

Translation: "A configuration C is the 4-tuple (q, w, O, G) consisting of the current state, remaining input, accumulated output, and active subordinate generators."

where
- $q\in Q$ is the current control state.  
    Translation: "q is the current control state from Q."

- $w \in \Sigma_{in}^*$ is the remaining input tape (possibly $\varepsilon$ for pure generation).  
    Translation: "w is the remaining input string over Σ_in (possibly empty)."

- $O$ is the accumulated output (a stream or tree under construction).  
    Translation: "O is the output produced so far (stream or structured tree)."

- $\mathcal{G}$ is a multiset (or stack) of active subordinate generators, each with its own configuration.  
    Translation: "G is the collection (multiset or stack) of active child generators and their configurations."

We write a single-step transition with the inference rule style:

$$
\frac{(q',a) \in \delta(q, x) \qquad \text{exec}(a, C) = C'}{(q, x \cdot w, O, \mathcal{G}) \longmapsto C'}
$$

Translation: "If (q', a) is one of the pairs returned by δ(q, x) and executing action a in configuration C produces configuration C', then the configuration (q, x·w, O, G) takes a single step and becomes C'."

Here $x$ is either the next input symbol or $\varepsilon$, and $\text{exec}(a,C)$ denotes the deterministic effect of performing action $a$ in configuration $C$ (append outputs, spawn child generators, or mutate $\delta$). Formalizing $\text{exec}$ precisely depends on the chosen execution model (synchronous vs asynchronous child execution, interleaving policy, resource accounting).  
Translation: "x is the consumed input symbol (or ε), and exec(a, C) denotes the deterministic result of applying action a to configuration C."

A run is a (finite or infinite) sequence of configurations $C_0, C_1, C_2,\dots$ starting from an initial configuration

$$C_0 = (q_0, w_0, \varnothing, \varnothing).$$

Translation: "A run is a sequence of configurations beginning with C₀, where C₀ has start state q₀, initial input w₀, and empty output and generator set."

The output of a terminating run is the final $O$; if runs spawn subgenerators, outputs are combined according to the machine's composition rules (e.g., appending child output as a subtree node).  
Translation: "The final output of a terminating run is the accumulated O; spawned generators' outputs are combined per the machine's composition rules."

## Example (formal trace)
Consider a tiny machine with $Q=\{S_0,S_1\}$, $\Sigma_{in}=\{\}$ (empty), $\Sigma_{out}=\{a,b\}$ and transitions

$$\delta(S_0,\varepsilon)=\{(S_0,\mathrm{emit}(a)\,;\,\mathrm{spawn}(A)),\; (S_1,\mathrm{emit}(a))\}$$

Translation: "When in state S₀ with no input (ε), δ returns two options: (S₀, emit(a); spawn(A)) meaning stay in S₀ while emitting an 'a' and spawning generator A, or (S₁, emit(a)) meaning move to S₁ and emit 'a'."

$$\delta(S_1,\varepsilon)=\{(S_1,\mathrm{emit}(b)),\; (\text{halt},\mathrm{emit}(b))\}$$

Translation: "When in state S₁ with no input, δ returns either (S₁, emit(b)) to stay in S₁ and emit 'b', or (halt, emit(b)) to emit 'b' and halt."

where $A$ is a subordinate generator that emits a finite sequence of $b$'s then halts. One possible run interleaves emitted $a$ and $b$ tokens to produce outputs like $a b b a b\dots$ depending on interleaving.  
Translation: "Generator A emits some number of 'b' tokens before halting; interleaving between parent and child emissions yields sequences like 'a b b a b ...'."

## Expressiveness and decidability
- In general, supergenerative automata with unbounded spawning and rewrite capabilities can simulate Turing-complete computation (one can encode unbounded tape and control by using spawned generators and rewrite rules). Therefore important decision problems such as global termination or membership (``does this machine ever emit a particular string $s$?'') are undecidable in full generality.  
    Translation: "With unlimited spawning and rewriting, the model can simulate a Turing machine, so properties like termination or whether a given string is ever emitted are undecidable."

- When the model is restricted (e.g., bounded spawn depth, finite-state-only rewriting that preserves a global bound, or resource limits on memory/time), many decision problems become decidable and sometimes tractable. Practical implementations therefore enforce resource bounds or use types of stratified rewriting that preserve termination.  
    Translation: "Imposing bounds (spawn depth, limited rewriting, resource caps) restores decidability for many questions."

## Common variants
- Deterministic vs nondeterministic: whether $\delta(q,x)$ contains at most one pair or multiple alternatives.  
    Translation: "Deterministic: δ(q,x) has at most one (next state, action) pair; nondeterministic: multiple pairs are possible."

- Probabilistic / stochastic: transitions include weights $p$ and the machine defines a distribution over outputs.  
    Translation: "Probabilistic variants attach probabilities p to alternatives, inducing a distribution over runs and outputs."

- Learning-enabled: transitions include parameters updated by an online learner (e.g., gradient updates, reinforcement signals).  
    Translation: "Learning-enabled machines adapt transition parameters online through learning algorithms."

- Resource-bounded / safe fragments: depth-limited spawning, linear-bounded rewriting, or types to ensure termination.  
    Translation: "Safe fragments restrict spawning and rewriting to guarantee termination and resource bounds."

## Complexity sketch and safety
- Unrestricted spawning + rewriting: Turing-complete → termination/membership undecidable.  
    Translation: "Without restrictions, the model is Turing-complete and key decision problems are undecidable."

- Bounded spawn depth $d$ and bounded state-space: emptiness/termination decidable; worst-case complexity depends on $d$ and underlying state cardinality.  
    Translation: "If spawn depth d and state space are bounded, emptiness and termination become decidable, with complexity depending on d and |Q|."

Practical safety mechanisms:
- Static checks: type systems that prevent unbounded self-replication, termination analysis via sized types.  
    Translation: "Static analyses (types, sized types) can rule out unbounded replication."

- Runtime checks: counters that prevent spawn beyond a depth or total instruction budget.  
    Translation: "Runtime enforcement (counters, budgets) stops excessive spawning or runtime cost."

## Implementation notes (API sketch)
An implementation-focused API treats a generator as an object with a transition function. Pseudocode (Python-like) sketch:

```python
class Generator:
        def __init__(self, state=q0):
                self.state = state

        def transition(self, symbol):
                # return list of (next_state, action) pairs
                pass

        def step(self, symbol):
                pairs = self.transition(symbol)
                for (s,a) in pairs:
                        self.state = s
                        execute_action(a)
```

Translation: "This sketch defines a Generator class whose transition method maps an input symbol to a list of (next_state, action) pairs; step applies each pair by updating state and executing the action."

Key implementation choices:
- Execution model for spawned generators: run-to-completion, cooperative interleaving, or dedicated scheduling.  
    Translation: "Decide whether spawned generators run to completion, interleave cooperatively, or are scheduled independently."

- Output representation: flat stream vs explicit tree (recommended for hierarchical outputs).  
    Translation: "Prefer structured tree representations for hierarchical outputs; streams are simpler but less structured."

- Mutation semantics: whether $\mathrm{rewrite}$ changes just the local generator or the global transition table.  
    Translation: "Clarify if rewrite affects only the local generator's δ or the global δ shared by many generators."

## Use cases & examples
- Program synthesis: spawn subgenerators that produce function bodies while the main generator composes higher-level scaffolding.  
    Translation: "Use spawning to have subgenerators synthesize nested program components."

- Structured text generation: produce documents with nested sections, where spawn creates section generators.  
    Translation: "Spawned section generators can produce nested document structure."

- Procedural content generation in games: spawn rooms, NPCs, or behavior trees hierarchically.  
    Translation: "Spawn hierarchical generators for rooms, NPCs, or behaviors in game worlds."

## Design checklist (for practical adoption)
1. Choose interleaving semantics for child generators (deterministic append, FIFO, depth-first, etc.).  
     Translation: "Decide a deterministic policy for how child outputs interleave with parent output."

2. Decide whether rewrites are allowed and, if so, scope them (local vs global).  
     Translation: "Define the scope and permission model for rewrite actions."

3. Enforce resource limits (depth, total actions, memory) to guarantee safety.  
     Translation: "Set runtime or static resource limits to guarantee termination and safety."

4. Provide logging/tracing to reconstruct output trees and diagnose nontermination.  
     Translation: "Include logging and trace data to debug runs and detect nontermination."

## Further reading and formal connections
- Transducers and tree transducers (e.g., top-down tree transducers).  
    Translation: "Connections: transducers that map input trees to output trees."

- Recursive state machines and hierarchical statecharts.  
    Translation: "Relation to recursive state machines and hierarchical statechart formalisms."

- Generative grammars (context-free, indexed grammars) and their tree-producing variants.  
    Translation: "Relation to grammar formalisms that produce nested structures."

- Probabilistic automata and stochastic transducers.  
    Translation: "Relation to probabilistic models of stateful generation."

---