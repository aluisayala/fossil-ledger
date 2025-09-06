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
entry_hash = SHA256(
prev_hash + '|' +
timestamp_utc + '|' +
canonical_json_without_entry_hash + '|' +
signature_or_empty
)

python
Copy code
- Output digest must be **lowercase hex**.

---

## 3-step verification

**Step 1 — Load receipt and rebuild canonical JSON**
- Read the receipt JSON.
- Make a shallow copy without `entry_hash`.
- Canonicalize with `sort_keys=True, separators=(',', ':')`.

**Step 2 — Recompute the `entry_hash`**
- Compute `signature_or_empty = ''` if `signature` is `null`.
- Concatenate exactly with `|` separators.
- SHA-256 hash → lowercase hex.
- Compare with the receipt’s `entry_hash`.

**Step 3 — (Optional) Append to ledger and update HEAD**
- Append one JSON line to `ledger.jsonl` with fields:
  - `prev_hash`, `entry_hash`, `timestamp_utc`, and the full `data` object (the whole receipt **including** `entry_hash`).
- Write the new `entry_hash` into `ledger.HEAD` (single line).

---

## Reference script (Python): `verify_entry.py`

```python
#!/usr/bin/env python3
import sys, json, hashlib, argparse, time, os

def canonicalize(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))

def recompute_entry_hash(entry):
    # 1) Shallow copy without entry_hash
    entry_no_hash = dict(entry)
    entry_no_hash.pop('entry_hash', None)

    # 2) signature_or_empty
    sig = entry.get('signature', None)
    if sig is None:
        sig = ''

    # 3) canonical JSON (of the copy without entry_hash)
    canonical = canonicalize(entry_no_hash)

    # 4) binding string
    prev_hash = entry['prev_hash']
    timestamp_utc = entry['timestamp_utc']
    binding = f"{prev_hash}|{timestamp_utc}|{canonical}|{sig}"

    # 5) sha256 lowercase hex
    return hashlib.sha256(binding.encode('utf-8')).hexdigest()

def append_ledger(entry, ledger_path, head_path):
    line_obj = {
        "prev_hash": entry["prev_hash"],
        "entry_hash": entry["entry_hash"],
        "timestamp_utc": entry["timestamp_utc"],
        "data": entry
    }
    with open(ledger_path, 'a', encoding='utf-8') as f:
        f.write(canonicalize(line_obj) + "\n")
    with open(head_path, 'w', encoding='utf-8') as f:
        f.write(entry["entry_hash"] + "\n")

def main():
    ap = argparse.ArgumentParser(description="Verify OPHI fossil receipt and optionally append to ledger")
    ap.add_argument("receipt", help="Path to JSON receipt (e.g., ophi_emotional_node_test_receipt.json)")
    ap.add_argument("--ledger", default="ledger.jsonl", help="Path to append-only ledger file")
    ap.add_argument("--head", default="ledger.HEAD", help="Path to HEAD file")
    ap.add_argument("--append", action="store_true", help="Append to ledger and update HEAD on success")
    args = ap.parse_args()

    with open(args.receipt, "r", encoding="utf-8") as f:
        entry = json.load(f)

    computed = recompute_entry_hash(entry)
    print("Computed entry_hash:", computed)
    print("Receipt entry_hash :", entry.get("entry_hash"))

    if computed != entry.get("entry_hash"):
        print("❌ MISMATCH — do not append to ledger.")
        sys.exit(1)

    print("✅ MATCH — hash verified.")
    if args.append:
        append_ledger(entry, args.ledger, args.head)
        print(f"🧾 Appended to {args.ledger}")
        print(f"🔗 Updated {args.head}")

if __name__ == "__main__":
    main()
Example usage
bash
Copy code
python3 verify_entry.py ophi_emotional_node_test_receipt.json --append
Tip: record exact model/embedding versions and α in notes.env (below) for full provenance.

makefile
Copy code

### `notes.env`
```env
# OPHI verification provenance (recorded at emission time)
TEXT_MODEL="GPT-5 Thinking"
OPHI_BUILD="OmegaNet Explorer v1.0"
CODON_MAP_VERSION="v1.1 (FINALIZED Codon Symbolic Map — ALL)"
EMBEDDING_ENGINE="GAA Emotion Vectorizer v1.0"
ALPHA="1.000"                # α used in Ω = (state + bias) * α (not part of hash)
HASH_FUNCTION="sha256"
CANON_RULE="json.dumps(sort_keys=True,separators=(,,:)) + UTF-8"
HASH_FORMULA="prev_hash|timestamp_utc|canonical_json_without_entry_hash|signature_or_empty"

# Run-specific pointers (align with your receipt)
RECEIPT_FILE="ophi_emotional_node_test_receipt.json"
LEDGER_FILE="ledger.jsonl"
HEAD_FILE="ledger.HEAD"
RUN_TIMESTAMP_UTC="2025-09-06T16:04:32Z"
FOSSIL_ENTRY_HASH="6f4cdb0b9af4a0309fb0abf5efcb5428a05293d9ff8b51ff75723da98423f977"
PREV_HASH="0000000000000000000000000000000000000000000000000000000000000000"

# Human notes for skeptics:
# - The α, model, and embedding identifiers are recorded here for transparency.
# - Verification only depends on the canonicalization rule + hash formula above.

