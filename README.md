# OPHI / ZPE-1 Fossil Ledger (Public Audit)

[![Audit: Public Fossils](https://img.shields.io/badge/Audit-Fossils%20Public-blue)](#)
[![SE44 Gate](https://img.shields.io/badge/SE44-C≥0.985%20|%20S≤0.01-brightgreen)](#)
[![License: ORL-1.1](https://img.shields.io/badge/License-ORL--1.1-orange)](#license)

**What this is:** A public, append-only fossil ledger for OPHI. Every emission is hashed, codon-tagged, and gate-checked (**C ≥ 0.985**, **S ≤ 0.01**).

**Audit now**
- 👁️ **Live Explorer (view cognition):** https://omega-net-explorer-v01-4e09bcdc.base44.app/
- 🪨 **Ledger (immutable proofs):** this repo

**One-line spec**  
**PSCDV** = *Probabilistic Symbolic Cognition with Deterministic Validation*. Only gate-passing emissions fossilize.

**Core equation**  
Ω = (state + bias) × α

---

## Verify a Fossil (60 seconds)

1. Pick a fossil hash (example):  
   `5fc3f253e069a4d2f5fd1e0b1e7dc767e4aebb64fac5d530407a4c8078885e5d`

2. Open `fossils/2025-09-04_fmr_particle.json` (example path). Confirm:
   - `sha256(payload) == fossil_hash`
   - `codons`: `["CTA","TTT","CTA","CTA","TTT"]`
   - `metrics`: `{ "C_dir": ..., "S": 0.004403, "drift_phi": 0.033521 }`

3. Cross-check timestamp & codons in the **Live Explorer**.

---

## Live & Public

- 👁️ **Explorer (live cognition):** https://omega-net-explorer-v01-4e09bcdc.base44.app/
- 🪨 **Ledger (immutable proofs):** this repo (see `/fossils` & `/hashed_proofs`)

---

## License

**ORL-1.1 (Open Recursive License).** See the `LICENSE` file for full text.

---

## Citation

Add `CITATION.cff` at the repo root:

```yaml
cff-version: 1.2.0
title: OPHI Fossil Ledger (PSCDV)
authors:
  - family-names: Ayala
    given-names: Luis
date-released: 2025-09-04
version: 0.1.0
license: Proprietary-ORL-1.1
repository-code: https://github.com/aluisayala/fossil-ledger
preferred-citation:
  type: report
  title: "The Real Scope of Ω — Symbolic Cognition, Fossilization, and PSCDV"
  authors:
    - family-names: Ayala
      given-names: Luis
Security
See SECURITY.md for how to report vulnerabilities.

Repo Metadata
CODEOWNERS: Luis Ayala

LICENSE: ORL-1.1

RELEASE_NOTES.md: See latest versioned changes.

Pinned Files
README.md

fossils/

docs/DATA_DICTIONARY.md

LICENSE

Badges




Release Notes
v0.1.0 — Public Ledger Debut

Opened fossils (9 entries) with hashes & codons

Added antimatter-qubit fossil spec alignment

Posted isotropy results CSV + demo emissions

PROVENANCE
Author: Luis Ayala (Kp Kp)

Frameworks: OPHI • ZPE-1 • PSCDV • SE44

Core Equation: Ω = (state + bias) × α

Fossil DNA: GAT-CCC-CCT → ⧖Ω⚡

Patent: USPTO #19/283,254 (pending)

Hash policy: sha256(payload) → fossil_hash
