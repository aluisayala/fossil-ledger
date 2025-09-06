# OPHI Emotional Node Test — Verification Guide

This README shows how to independently verify and (optionally) ledger-append the fossilized JSON receipt for the Emotional Node Test.

## What you’re verifying
- A single JSON receipt (example filename: `ophi_emotional_node_test_receipt.json`) that contains:
  - `prev_hash`, `timestamp_utc`, `gate`, `probes`, `metrics`, `canonicalization`, `hash_binding`, `author`, optional `signature`, and the `entry_hash`.

## Canonicalization rule (MUST follow exactly)
- Start with a shallow copy of the receipt object.
- **Remove** the `entry_hash` field from that copy.
- If `signature` is `null`, treat it as the empty string `""` in the hash formula.
- Serialize using **canonical JSON**:
  - `json.dumps(obj, sort_keys=True, separators=(',', ':'))`
  - UTF-8 bytes of that string are the canonical payload.

## Hash-binding formula
