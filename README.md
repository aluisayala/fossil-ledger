# OPHI Proof-of-Fossilization Node (Render Edition)

This node provides a public API for creating and verifying SE44-gated symbolic fossils.

## Endpoints
- `GET /` → Health check
- `POST /fossilize` → Create fossil (JSON payload)
- `POST /verify` → Verify SHA-256 integrity

Each fossil includes:
- SE44 validation (C ≥ 0.985, S ≤ 0.01)
- Real SHA-256 hash
- RFC-3161 timestamp
- ECDSA signature + public key (passed in from frontend)

## Deploy on Render
1. Create a new **Web Service**
2. Connect this folder’s repo
3. Build Command:
   pip install -r requirements.txt
4. Start Command:
   uvicorn api:app --host 0.0.0.0 --port 10000
5. Deploy → You’ll get a live URL:
   https://ophi-miner-node.onrender.com

## Example Test
```bash
curl -X POST https://ophi-miner-node.onrender.com/fossilize \
-H "Content-Type: application/json" \
-d '{"codon_sequence":["ATG","CCC","TTG"],"state":0.5,"bias":0.2,"alpha":1.25,"coherence":0.99,"entropy":0.005,"creator_pubkey":"demo","signature":"demo"}'
```
