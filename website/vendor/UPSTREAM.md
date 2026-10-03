The vendored Python verifier is sourced from:
https://github.com/hamadalmunyif/paygod-kernel-mvp/blob/main/tools/verify_portable_evidence.py

Verifier upstream Git blob: b388cf490a9cb87a3c5ded1b6e285db9cd262fc6
Issuer-auth helper upstream Git blob: 807d333a243f1e13d7b3682505c1318c3021fd98
Version: 0.4.0
Canonicalization profile: paygod-c14n-v1
Issuer signature profile: paygod-ed25519-receipt-v1
Trust-store profile: paygod-ed25519-trust-v1
Crypto dependency: cryptography==50.0.2
License: Apache-2.0 (see LICENSE).

Integrity and issuer authenticity are separate verification dimensions.
A verified issuer signature means a recipient-trusted Ed25519 key signed the exact receipt commitment.
It does not prove external fact truth, policy replay, regulator authorization, trusted third-party time,
or permission to execute.
