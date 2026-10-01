# PayGod evidence handoff — pilot brief

Use one real decision to establish whether a portable evidence package is useful to a recipient outside the originating system. This is a planning template, not an implementation or compliance certification.

## 1. Define the decision

- Decision or claim:
- Current workflow and system:
- Who needs to inspect the result, and why:
- Cost or delay caused by the current evidence handoff:

## 2. Identify the source

- Measurement or input, including units and period:
- Source system, instrument or responsible issuer:
- How source identity and measurement quality are established:
- Required supporting records:
- Sensitive fields that must be excluded or handled separately:

## 3. Make the reasoning explicit

- Contract and required input fields:
- Rule or policy, its version and owner:
- Expected decision and reason:
- What can and cannot be inferred from these inputs:

## 4. Agree on the recipient's checks

- Independent recipient:
- Files and decision bindings they need to inspect:
- Provenance, signatures or trust roots they require beyond integrity:
- What a passed check permits them to conclude:
- What it does not permit them to conclude or execute:

## 5. Set acceptance criteria

- The recipient can inspect an exported bundle without the producer session.
- The supported checks pass for the agreed valid fixture.
- An altered committed artifact is detected.
- A substituted decision is detected.
- Issuer identity and source truth are either separately established or explicitly unverified.
- Domain owner and recipient agree whether the evidence is useful for this workflow.

Record the result before expanding to another use case. The current browser verifier is a demonstration profile. Production hardening and domain validation are separate work.
