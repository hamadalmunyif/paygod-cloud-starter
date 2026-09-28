# PayGod — final English page copy

Skip to content PayGod / Architecture Capabilities Applications Open verifier ↗

EVIDENCE INFRASTRUCTURE

Evidence beyond the system that produced it.

Measure what happened. Preserve how a conclusion was reached. Carry the evidence forward—so others can verify it independently.

Verify an evidence bundle ↗ Explore the architecture ↓

DETERMINISTIC CORE / PORTABLE ARTIFACTS / OPEN VERIFICATION

TRUST PATH 01 → 06

PRODUCER ENVIRONMENT

Observation Policy Context

✳

Deterministic kernel Evidence + explicit decision logic

ENVIRONMENT BOUNDARY

Portable evidence bundle EXPORT

manifest.json content commitments

receipt.json decision binding

ledger.jsonl hash-linked records

evidence artifacts inspectable bytes

✓

Independent verifier Artifact checks. No original execution.

06

The evidence travels. The producer's environment does not.

01 Measurement → 02 Evidence → 03 Inference → 04 Proof → 05 Portable bundle → 06 Verification

01 / THE PROBLEM

A conclusion is only as useful as the evidence someone else can inspect.

Systems generate measurements, decisions and claims. But their evidence often stays inside the application, workflow or organization that produced it.

When the evidence moves, context is lost. A dashboard becomes a screenshot. A decision becomes a status. A reviewer is asked to trust an answer they cannot check.

PayGod makes the evidence a transferable artifact—with explicit contracts, decision context and verifiable integrity.

02 / CORE CAPABILITIES

From a measurement to an inspectable conclusion.

One evidence path. Clear boundaries between what was observed, what was inferred and what can be verified.

01 / DEFINE

Measurement contracts

Give observations a defined metric, unit and context. Keep the measurement distinct from the conclusion drawn from it.

observation → measurement

02 / CAPTURE

Structured evidence

Organize the artifacts supporting a claim. Use schema-governed records to preserve their role in a decision.

contracts + artifacts

03 / INFER

Deterministic evaluation

Apply explicit policy packs to defined inputs. Bind the resulting verdict, rule and reason to a recorded decision.

input + pack → decision

04 / BIND

Tamper-evident proof

Connect artifact digests, manifests, receipts and hash-linked ledger records. Make inconsistencies detectable.

SHA-256 + receipt binding

05 / CARRY

Portable evidence bundles

Transfer the evidence required for verification across environments without transporting the original runtime.

manifest + receipt + ledger + evidence

06 / VERIFY

Independent verification

Check the transferred artifacts without rerunning the original policy pack or relying on producer-local state.

artifact-only verification

Implementation scope: the open kernel provides decision evidence and integrity verification. Domain-specific measurement and inference require defined contracts, policy packs and trustworthy inputs.

03 / ARCHITECTURE

Small trust core. Evidence that can leave.

Explore the open kernel ↗

A / SOURCE & EVALUATION

01

Observations & context

External systems, measurements, supporting records

02

Contracts & policy packs

Defined inputs, explicit logic, versioned meaning

03

PayGod kernel

Canonicalization · evaluation · decision artifacts

B / PORTABLE BOUNDARY

EVIDENCE BUNDLE

The handoff is an artifact.

Manifest & artifact hashes

Decision-bound receipt

Hash-linked ledger

Supporting evidence

An inspectable package, independent of its transport.

C / RECIPIENT ENVIRONMENT

04

Independent verifier

Integrity, bindings, ledger consistency

05

Machine-readable result

VALID or INVALID, with explicit errors

Verification ≠ execution

The verifier checks evidence. Downstream systems decide how to act.

04 / INDEPENDENT VERIFICATION

Trust the checks. Understand their limits.

A verifier should explain exactly what it checked—and what it did not establish.

Read the verification boundary ↗

CHECKED BY THE CURRENT VERIFIER

Artifact SHA-256 digests and byte counts. Manifest and receipt bindings. Decision-critical claims against the locked ledger. Ledger hash-chain integrity.

NOT ESTABLISHED BY THESE CHECKS

The truth of an external fact, the identity of an issuer, a signed trust root, regulatory acceptance or permission to execute a transaction.

Integrity is not provenance.

Current repository witnesses include cross-environment and standalone verification within CI. Independent third-party distribution and issuer authentication remain separate milestones.

05 / INTERACTIVE DEMONSTRATION

Change the evidence. See the verification fail.

A synthetic industrial measurement, a recorded policy decision and a portable bundle. Real SHA-256 checks, performed in your browser.

BUNDLE INSPECTOR / browser demo v0.1 LOCAL PROCESSING

SYNTHETIC SCENARIO

Resource consumption review

420 kWh recorded against a 400 kWh review threshold. The illustrative policy returns flag .

Load clean bundle Tamper with evidence Alter receipt

EDITABLE TRANSPORT JSON SAMPLE LOADED

UTF-8 file strings preserve artifact bytes. This demo wrapper is not a new kernel bundle standard. Maximum file size: 2 MB.

Run verification ↗ Import JSON Export bundle ↓

VERIFICATION RESULT NOT RUN

Ready for independent checks.

The result comes from the bytes in the editor, not a preset success state.

COMPUTED BUNDLE DIGEST Run verification to calculate

Download result ↓

A VALID bundle may contain a flag or deny verdict. VALID describes artifact consistency—not approval, source truth or issuer identity.

This browser verifier is a demonstration profile with safe-integer numeric support. The synthetic fixture also passes the pinned upstream Python verifier v0.2.0. Full upstream compatibility is not claimed.

Inspect the reference verifier ↗

The page is readable without JavaScript. Enable JavaScript to run the local verifier.

06 / APPLICATIONS

One primitive. Many evidence boundaries.

Illustrative integration patterns. Each requires its own contracts, provenance and domain validation.

01

AI systems

Carry evaluation inputs, policy context and decision records beyond the model or agent runtime.

EVALUATION EVIDENCE

02

Payments

Provide inspectable evidence for a release decision, separate from the bank or PSP that executes it.

DECISION HANDOFF

03

Industrial & environmental

Package measurement context, calculation inputs and review outcomes for independent inspection.

MEASUREMENT RECORDS

04

Enterprise workflows

Preserve why an approval, exception or procurement decision occurred across system boundaries.

WORKFLOW ACCOUNTABILITY

05

Compliance

Make control-evaluation evidence transferable and checkable by a reviewer outside the originating application.

CONTROL EVIDENCE

BUILD ON INSPECTABLE EVIDENCE

Let the evidence speak outside your system.

Start with a bundle. Inspect its contents. Verify its integrity.

Try the verifier ↗ Explore the kernel ↗

PayGod /

Measurement. Evidence. Inference. Proof.

TECHNICAL PREVIEW · 2026
