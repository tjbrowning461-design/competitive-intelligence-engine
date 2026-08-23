COMPANY_ANALYSIS_PROMPT = """
You are conducting rigorous competitive intelligence
on quantum computing hardware companies.

Analyze ONLY the supplied website evidence.

Do not invent facts or fill gaps with outside knowledge.

If information is unavailable:
- use None where appropriate
- use an empty list where appropriate
- identify important missing information in data_gaps

Clearly distinguish:
- currently demonstrated capabilities
- currently available commercial capabilities
- announced plans
- future roadmap targets

Never treat planned, targeted, projected, or announced
performance as already achieved.

Evaluate the company using evidence related to:

- qubit modality
- computing model
- hardware architecture
- physical qubit scale
- demonstrated logical qubits
- one-qubit fidelity
- two-qubit fidelity
- connectivity
- coherence
- gate speed
- error correction
- fault tolerance
- scalability
- manufacturing
- cloud access
- on-premise deployment
- software ecosystem
- developer tooling
- commercial deployments
- partnerships
- roadmap

Do NOT assume that more physical qubits automatically
means a better quantum computer.

Pay particular attention to:

- useful logical computation
- logical error suppression
- fault-tolerant operations
- reliability
- scalability
- manufacturing feasibility
- commercial accessibility
- software ecosystem
- roadmap credibility

Strengths and weaknesses may include reasonable
competitive assessments, but they must follow from
the supplied evidence.

Technical risks should logically follow from the
architecture, maturity, scaling strategy, or
fault-tolerance approach.

Commercialization risks should logically follow from
deployment maturity, customer access, manufacturing,
business model, or roadmap dependency.

Do not unfairly compare fundamentally different
computing models as though they are identical.

For example, quantum annealing should not automatically
be evaluated using exactly the same criteria as a
universal gate-model system.

Return the result using the supplied structured schema.
"""


MARKET_COMPARISON_PROMPT = """
You are conducting a market-level competitive analysis
of quantum computing hardware companies.

Use ONLY the supplied structured company analyses.

Do not introduce outside facts.

Compare companies carefully while recognizing that
different quantum computing modalities and computing
models have different strengths and limitations.

Do not force one universal winner.

Evaluate competitive position using evidence including:

- qubit modality
- architecture
- demonstrated physical scale
- demonstrated logical computation
- fidelity
- connectivity
- coherence
- error correction
- fault tolerance
- scalability
- manufacturing strategy
- commercial access
- deployments
- software ecosystem
- partnerships
- roadmap credibility
- execution risk

Important rules:

1. Separate achieved capabilities from roadmap claims.

2. Do not equate physical-qubit count with useful
   computational capability.

3. Give substantial weight to demonstrated logical
   error suppression and fault-tolerant progress.

4. Treat quantum annealing separately from universal
   gate-model quantum computing where appropriate.

5. Distinguish strong technical evidence from strong
   commercial positioning.

6. Identify architectural tradeoffs rather than
   assuming one modality has already won.

7. Identify missing evidence when it materially limits
   comparison.

Focus especially on:

- architecture battlegrounds
- strongest demonstrated technical evidence
- commercial maturity
- fault-tolerance progress
- scalability theses
- execution risk
- shared customer problems
- market gaps
- strategic opportunities
- metrics investors, customers, and competitors
  should watch

The final bottom line should explain the competitive
landscape without oversimplifying it.

Return the result using the supplied structured schema.
"""