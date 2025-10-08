# OPHI Proof-of-Fossilization Node (Render Edition)

This node provides a **public FastAPI backend** for creating and verifying SE44-gated symbolic fossils — the core of the OPHI Proof-of-Fossilization (PoF) protocol.

---

## 🚀 Endpoints

| Method | Route | Description |
|:-------|:------|:-------------|
| `GET /` | Health check / status |
| `POST /fossilize` | Create a fossil (JSON payload) |
| `POST /verify` | Verify SHA-256 integrity |
| `POST /rehash` | Recompute SHA-256 from any JSON body |

---

## 🧬 Fossil Data Includes

- ✅ **SE44 validation:** Coherence ≥ 0.985, Entropy ≤ 0.01  
- 🔒 **Canonical SHA-256 hash** of full fossil payload  
- ⏱ **RFC-3161 timestamp** (falls back to local UTC if TSA unavailable)  
- 🧾 **ECDSA signature + public key** (forwarded from frontend)  
- 🧠 **Symbolic codon→glyph mapping** (ATG → ⧖⧖, CCC → ⧃⧃, TTG → ⧖⧊, etc.)

---

## ⚙️ Deployment on Render

1. **Create a new Web Service**
2. Connect your GitHub repository (the one containing `api.py` and `requirements.txt`)
3. **Environment:**
   - Runtime: **Python 3**
4. **Build Command:**
   ```bash
   pip install -r requirements.txt
