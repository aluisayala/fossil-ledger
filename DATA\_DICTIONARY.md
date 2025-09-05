# DATA\_DICTIONARY.md

## ophi\_emissions\_demo.csv

* `emission_id`: string
* `timestamp_utc`: ISO 8601 timestamp
* `omega_result`: float — unitless scalar result from Ω equation
* `drift_phi`: float — symbolic phase drift measure
* `entropy_S`: float — entropy of emission, in bits (≤ 0.01 to pass)
* `coherence_C`: float — coherence score (≥ 0.985 to pass)
* `fossil_hash`: string — SHA-256 hex digest of payload
* `codon_triads`: string — hyphen-separated codons (e.g., "CTA-TTT-CTA")

## ophi\_isotropy\_scores.csv

* `phi_iso`: float — global isotropy score \[0,1]
* `F_iso`: float — fraction of emissions that passed local isotropy check
* `run_id`: string — UUID of the mesh run
* `timestamp_utc`: ISO 8601 timestamp

## se44\_validated\_fossils.csv

* `fossil_hash`: string — verified hash of fossil emission
* `C`: float — coherence value
* `S`: float — entropy value
* `codons`: string\[] — codon array, order-preserved
* `validator_passed`: boolean — whether both validators accepted the fossil

Each CSV assumes standard UTF-8 encoding and comma-separated formatting. Units and gate thresholds are consistent with OPHI's SE44 configuration.
