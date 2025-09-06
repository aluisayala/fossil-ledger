# OPHI Emotional Node Test — Verification Guide

This README explains how to independently verify (and optionally ledger-append) the fossilized JSON receipt.

## What you’re verifying
A JSON receipt with at least: `prev_hash`, `timestamp_utc`, `gate`, `probes`, `metrics`, `canonicalization`, `hash_binding`, `author`, optional `signature`, and `entry_hash`.

## Canonicalization rule (MUST match exactly)
- Start with a shallow copy of the receipt object.
- **Remove** the `entry_hash` field from that copy.
- If `signature` is `null`, treat it as the empty string `""` in the hash formula.
- Serialize using **canonical JSON with Unicode intact**:
  - `json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`
  - Use **UTF-8 bytes** of that string as the canonical payload.

## Hash-binding formula
entry_hash = SHA256(
prev_hash + '|' +
timestamp_utc + '|' +
canonical_json_without_entry_hash + '|' +
signature_or_empty
)

markdown
Copy code
Output digest must be **lowercase hex**.

---

## Verification steps

**Step 1 — Load and rebuild canonical JSON**
- Read the receipt JSON.
- Make a shallow copy without `entry_hash`.
- Canonicalize with `sort_keys=True, separators=(',', ':'), ensure_ascii=False`.
- Encode to UTF-8 bytes.

**Step 2 — Recompute `entry_hash`**
- Use `''` (empty string) if `signature` is `null`.
- Concatenate with `|` separators as in the formula above.
- SHA-256 → lowercase hex.
- Compare with the receipt’s `entry_hash`.

**Step 3 — (Optional) Append to ledger and update HEAD**
- Append one JSON line to `ledger.jsonl` containing:
  - `prev_hash`, `entry_hash`, `timestamp_utc`, and either:
    - `data` = full receipt (default), or
    - `data_ptr` (path/URI), or
    - `data_uri` (Base64 of canonical JSON).
- Write the new `entry_hash` into `ledger.HEAD` (single line).

### Ledger size note (optional)
Storing full receipts is simple but can bloat the ledger. Later you can use `--ledger-mode data_uri` (or `ptr`) to keep lines smaller; trade-offs are described in the script help.

### Example
python3 verify_entry.py ophi_emotional_node_test_receipt.json --append --ledger-mode full

Copy code
verify_entry.py
python
Copy code
#!/usr/bin/env python3
import sys, json, hashlib, argparse, os, base64

def canonicalize(obj) -> str:
    # Canonical JSON: sorted keys, no extra spaces, keep Unicode (ensure_ascii=False)
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def recompute_entry_hash(entry: dict) -> str:
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

def append_ledger(entry: dict, ledger_path: str, head_path: str, mode: str, receipt_path: str):
    line_obj = {
        "prev_hash": entry["prev_hash"],
        "entry_hash": entry["entry_hash"],
        "timestamp_utc": entry["timestamp_utc"],
    }

    if mode == "full":
        line_obj["data"] = entry
    elif mode == "ptr":
        # Keep line tiny; relies on external receipt file or URI being preserved.
        line_obj["data_ptr"] = receipt_path
    elif mode == "data_uri":
        # Embed canonical JSON (without entry_hash) as a data URI (UTF-8 Base64).
        entry_no_hash = dict(entry)
        entry_no_hash.pop('entry_hash', None)
        canonical = canonicalize(entry_no_hash)
        b64 = base64.b64encode(canonical.encode('utf-8')).decode('ascii')
        line_obj["data_uri"] = f"data:application/json;charset=utf-8;base64,{b64}"
    else:
        raise ValueError("Unknown ledger mode")

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
    ap.add_argument("--ledger-mode", choices=["full", "ptr", "data_uri"], default="full",
                    help="Ledger storage mode: full receipt (default), path/URI pointer, or embedded Base64 data URI")
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
        append_ledger(entry, args.ledger, args.head, args.ledger_mode, args.receipt)
        print(f"🧾 Appended to {args.ledger} (mode={args.ledger_mode})")
        print(f"🔗 Updated {args.head}")

if __name__ == "__main__":
    main()
notes.env
env
Copy code
# OPHI verification provenance (recorded at emission time)
TEXT_MODEL="GPT-5 Thinking"
OPHI_BUILD="OmegaNet Explorer v1.0"
CODON_MAP_VERSION="v1.1 (FINALIZED Codon Symbolic Map — ALL)"
EMBEDDING_ENGINE="GAA Emotion Vectorizer v1.0"
ALPHA="1.000"                                  # α used in Ω = (state + bias) * α (not part of hash)
HASH_FUNCTION="sha256"
CANON_RULE="json.dumps(sort_keys=True,separators=(,,:),ensure_ascii=False) + UTF-8"
HASH_FORMULA="prev_hash|timestamp_utc|canonical_json_without_entry_hash|signature_or_empty"

# Run-specific pointers (align with your receipt)
RECEIPT_FILE="ophi_emotional_node_test_receipt.json"
LEDGER_FILE="ledger.jsonl"
HEAD_FILE="ledger.HEAD"
RUN_TIMESTAMP_UTC="2025-09-06T16:04:32Z"
FOSSIL_ENTRY_HASH="<RECOMPUTE_WITH_UNICODE_CANON>"   # will differ if previous hash used ensure_ascii=True
PREV_HASH="0000000000000000000000000000000000000000000000000000000000000000"

# Human notes:
# - Canonicalization MUST set ensure_ascii=False so characters like Ω are not escaped, preserving the exact bytes used for hashing.
# - If you previously computed entry_hash without ensure_ascii=False, it will NOT verify—recompute with this rule.
