# PayGod — English page copy

PayGod — Evidence beyond the system.

Skip to content

PayGod

/

Architecture

Capabilities

Applications

Open verifier

EVIDENCE INFRASTRUCTURE

Evidence beyond

the system

that produced it.

Give another party the evidence they need to check your result. Package the recorded inputs, decision context and integrity checks so the evidence can travel beyond your system.

Try an evidence handoff

Explore the architecture

↓

DETERMINISTIC CORE

/

PORTABLE ARTIFACTS

/

OPEN VERIFICATION

TRUST PATH

01 → 06

PRODUCER ENVIRONMENT

Observation

Policy

Context

✳

Deterministic kernel

Evidence + explicit decision logic

ENVIRONMENT BOUNDARY

Portable evidence bundle

EXPORT

manifest.json

content commitments

receipt.json

decision binding

ledger.jsonl

hash-linked records

evidence artifacts

inspectable bytes

✓

Independent verifier

Artifact checks. No original execution.

06

The evidence travels. The producer's environment does not.

01

Measurement

→

02

Evidence

→

03

Inference

→

04

Proof

→

05

Portable bundle

→

06

Verification

ONE DECISION. TWO ENVIRONMENTS.

From an internal result

to someone else's checks.

An operations team records a measurement. A reviewer needs to inspect the evidence outside that team's application.

01 / PRODUCER

Record the result.

Keep the input, rule reference and decision together.

420 kWh · recorded decision: FLAG

02 / HANDOFF

Send the package.

Download the evidence files and their integrity commitments.

One portable bundle

03 / RECIPIENT

Check what arrived.

Import the file into a separate verifier. No producer session required.

Integrity checked · provenance explicit

Illustrative industrial workflow. The demo below uses a synthetic fixture.

01 / THE PROBLEM

A conclusion is only

as useful as the evidence

someone else can inspect.

Systems generate measurements, decisions and claims. But their evidence often stays inside the application, workflow or organization that produced it.

When the evidence moves, context is lost. A dashboard becomes a screenshot. A decision becomes a status. A reviewer is asked to trust an answer they cannot check.

PayGod makes the evidence a transferable artifact—with explicit contracts, decision context and verifiable integrity.

02 / CORE CAPABILITIES

From a measurement

to an inspectable conclusion.

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

Small trust core.

Evidence that can leave.

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

The handoff is

an artifact.

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

Trust the checks.

Understand their limits.

A verifier should explain exactly what it checked—and what it did not establish.

Read the verification boundary ↗

CHECKED BY THE CURRENT VERIFIER

Artifact SHA-256 digests and byte counts. Manifest and receipt bindings. Decision-critical claims against the locked ledger. Ledger hash-chain integrity.

NOT ESTABLISHED BY THESE CHECKS

The truth of an external fact, the identity of an issuer, a signed trust root, regulatory acceptance or permission to execute a transaction.

Integrity is not provenance.

Current repository witnesses include cross-environment and standalone verification within CI. Independent third-party distribution and issuer authentication remain separate milestones.

05 / TRY THE HANDOFF

Download the evidence.

Check it somewhere else.

Start with a readable card. Inspect or change the sample, download the bundle, then open it in the separate verifier.

PRODUCER WORKSPACE

/ demo profile v0.2

PROCESSED ON THIS DEVICE

SYNTHETIC INDUSTRIAL EXAMPLE

One measurement. A review decision.

The sample records 420 kWh against a fictional 400 kWh review threshold. The recorded decision is FLAG. This is a prepared fixture, not a live meter or policy execution.

Load clean bundle

Change the measurement

Change the decision

Choose bundle file

JSON file · up to 2 MB

WAITING FOR EVIDENCE

No bundle loaded.

Choose a downloaded bundle or paste its JSON below. Nothing is sent to a server.

EVIDENCE CARD

SELF-DECLARED CONTENT

Recorded decision

Rule reference

Declared source

Recorded time

Package contents

This card reads the supplied files. It does not establish that the measurement happened or the source is authentic.

Run verification

Download this bundle

View or edit technical files

NO BUNDLE

BUNDLE TRANSPORT JSON

UTF-8 file strings preserve artifact bytes. This demo transport is not a new kernel standard. Maximum total size: 2 MB.

WHAT CAN BE VERIFIED?

NOT RUN

Waiting for a bundle.

Choose a bundle to begin the checks.

File and record integrity

Not checked

Receipt matches the decision record

Not checked

Issuer identity

Not verified

Real-world observation

Not verified

Inspect technical checks

0 checks

MANIFEST COMMITMENT

Not calculated

Digest of the declared file commitments. Individual file checks detect changes to the actual bytes.

Download verification report

VALID means the supported consistency checks passed. A valid bundle can still contain a FLAG or DENY decision. It is not approval, authenticated provenance or proof of a real-world fact.

NEXT / THE RECIPIENT'S SIDE

The file carries the evidence.

Download this bundle above, then choose that file in the separate verifier. It opens empty and does not inherit the producer's results.

Open separate verifier

Download offline verifier

This is a browser demonstration with safe-integer numeric support. The synthetic fixture also passes the pinned Python verifier v0.2.0. Separate execution is demonstrated; a third-party audit and full upstream compatibility are not claimed.

Inspect the reference verifier

Enable JavaScript to inspect and verify the local bundle.

06 / APPLICATIONS

One primitive.

Many evidence boundaries.

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

START WITH ONE EVIDENCE HANDOFF

Bring one decision.

Define the evidence.

Choose a source, an explicit rule and a recipient who needs to check the result. Use the pilot brief to scope a real workflow before building an integration.

01 · Identify the source

02 · Define the decision

03 · Agree on recipient checks

Get the pilot brief

Explore the kernel

PayGod

/

Measurement. Evidence. Inference. Proof.

TECHNICAL PREVIEW · 2026
