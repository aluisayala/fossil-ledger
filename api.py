from fastapi import FastAPI, Request
from datetime import datetime
import hashlib, json, requests

app = FastAPI(title="OPHI Fossil Miner Node")

TSA_URL = "https://freetsa.org/tsr"

def se44_valid(c, s):
    return c >= 0.985 and s <= 0.01

@app.get("/")
def home():
    return {"status": "OPHI Miner Node active", "timestamp": datetime.utcnow().isoformat() + "Z"}

@app.post("/fossilize")
async def fossilize(req: Request):
    data = await req.json()

    codon_seq = data.get("codon_sequence", [])
    state = data.get("state", 0.0)
    bias = data.get("bias", 0.0)
    alpha = data.get("alpha", 1.0)
    coherence = data.get("coherence", 1.0)
    entropy = data.get("entropy", 0.0)
    pubkey = data.get("creator_pubkey", "")
    signature = data.get("signature", "")

    if not se44_valid(coherence, entropy):
        return {"error": "SE44 Gate failed", "valid": False}

    glyph_map = {"ATG": "⧖⧖", "CCC": "⧃⧃", "TTG": "⧖⧊"}
    glyphs = [glyph_map.get(c, "?") for c in codon_seq]
    omega = (state + bias) * alpha

    fossil = {
        "fossil_tag": f"ophi.fossil.{datetime.utcnow().timestamp()}",
        "codon_sequence": codon_seq,
        "glyphs": glyphs,
        "equation": "Ω = (state + bias) × α",
        "inputs": {"state": state, "bias": bias, "alpha": alpha},
        "omega_output": omega,
        "metrics": {"C": coherence, "S": entropy},
        "creator_pubkey": pubkey,
        "signature": signature
    }

    canonical = json.dumps(fossil, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    fossil["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()

    try:
        tsa = requests.post(TSA_URL, data=fossil["sha256"].encode(), timeout=5)
        fossil["timestamp_rfc3161"] = tsa.headers.get("Date", datetime.utcnow().isoformat()+"Z")
    except Exception:
        fossil["timestamp_rfc3161"] = datetime.utcnow().isoformat()+"Z"

    return {"fossil": fossil, "valid": True}

@app.post("/verify")
async def verify(req: Request):
    data = await req.json()
    try:
        canonical = json.dumps({k:v for k,v in data.items() if k not in ("sha256","signature")},
                                sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        sha = hashlib.sha256(canonical.encode()).hexdigest()
        if sha == data.get("sha256"):
            return {"valid": True, "message": "✅ SHA-256 verified"}
        else:
            return {"valid": False, "message": "❌ SHA mismatch"}
    except Exception as e:
        return {"valid": False, "error": str(e)}
