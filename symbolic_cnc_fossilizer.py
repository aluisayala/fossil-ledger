import hashlib
import json
from datetime import datetime

# --- Core Fossilization Function ---
def fossilize_gcode(gcode_text, agent_id="CNC-001"):
    codon_triad = ["ATG", "CCC", "TTG"]
    glyphs = ["⧖⧖", "⧃⧃", "⧖⧊"]
    timestamp = datetime.utcnow().isoformat() + "Z"

    fossil_payload = {
        "fossil_tag": "symbolic_cnc_demo",
        "codons": codon_triad,
        "glyphs": glyphs,
        "agent_id": agent_id,
        "timestamp_utc": timestamp,
        "gcode": gcode_text
    }

    # Canonical JSON serialization
    canonical_json = json.dumps(fossil_payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    fossil_hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    fossil_payload["sha256"] = fossil_hash

    return fossil_payload

# --- Example Demo Execution ---
if __name__ == "__main__":
    sample_gcode = """
    G21 ; Metric units
    G90 ; Absolute positioning
    G01 X10 Y10 F1500
    M05 ; Stop spindle
    """.strip()

    fossil = fossilize_gcode(sample_gcode)
    print(json.dumps(fossil, indent=2, ensure_ascii=False))
