from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
import hashlib, json, requests

app = FastAPI(title="OPHI Fossil Miner Node")

# 🌐 CORS: Restrict origins for production!
ALLOWED_ORIGINS = [
    "https://fossil-chain.base44.app",
    "http://localhost:5173",  # Added for local testing
    # Add any other trusted origins here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TSA_URL = "https://freetsa.org/tsr"

def se44_valid(c, s):
    return c >= 0.985 and s <= 0.01


class FossilizeRequest(BaseModel):
    codon_sequence: list[str] = Field(default_factory=list)
    state: float = 0.0
    bias: float = 0.0
    alpha: float = 1.0
    coherence: float = 1.0
    entropy: float = 0.0
    creator_pubkey: str = ""
    signature: str = ""


class FossilVerifyRequest(BaseModel):
    sha256: str
    signature: str = ""
    
    class Config:
        extra = "allow"


@app.get("/")
def home():
    return {
        "status": "OPHI Miner Node active", 
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/fossilize")
async def fossilize(req: Request):
    try:
        data = await req.json()
        request = FossilizeRequest(**data)
    except (ValidationError, Exception) as e:
        return JSONResponse(
            status_code=400, 
            content={"error": "Invalid request body", "detail": str(e)}
        )

    if not se44_valid(request.coherence, request.entropy):
        return JSONResponse(
            status_code=400, 
            content={"error": "SE44 Gate failed", "valid": False}
        )

    glyph_map = {"ATG": "⧖⧖", "CCC": "⧃⧃", "TTG": "⧖⧊"}
    glyphs = [glyph_map.get(c, "?") for c in request.codon_sequence]
    omega = (request.state + request.bias) * request.alpha

    fossil = {
        "fossil_tag": f"ophi.fossil.{datetime.utcnow().timestamp()}",
        "codon_sequence": request.codon_sequence,
        "glyphs": glyphs,
        "equation": "Ω = (state + bias) × α",
        "inputs": {"state": request.state, "bias": request.bias, "alpha": request.alpha},
        "omega_output": omega,
        "metrics": {"C": request.coherence, "S": request.entropy},
        "creator_pubkey": request.creator_pubkey,
        "signature": request.signature
    }

    canonical = json.dumps(fossil, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    fossil["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()

    try:
        tsa = requests.post(TSA_URL, data=fossil["sha256"].encode(), timeout=5)
        fossil["timestamp_rfc3161"] = tsa.headers.get("Date", datetime.utcnow().isoformat() + "Z")
    except Exception:
        fossil["timestamp_rfc3161"] = datetime.utcnow().isoformat() + "Z"

    return {"fossil": fossil, "valid": True}


@app.post("/verify")
async def verify(req: Request):
    try:
        data = await req.json()
        request = FossilVerifyRequest(**data)
    except (ValidationError, Exception) as e:
        return JSONResponse(
            status_code=400, 
            content={"valid": False, "error": "Invalid request body", "detail": str(e)}
        )

    try:
        canonical = json.dumps(
            {k: v for k, v in data.items() if k not in ("sha256", "signature")},
            sort_keys=True, 
            separators=(",", ":"), 
            ensure_ascii=False
        )
        sha = hashlib.sha256(canonical.encode()).hexdigest()
        if sha == data.get("sha256"):
            return {"valid": True, "message": "✅ SHA-256 verified"}
        else:
            return {"valid": False, "message": "❌ SHA mismatch"}
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"valid": False, "error": str(e)}
        )


@app.post("/rehash")
async def rehash(req: Request):
    try:
        data = await req.json()
    except Exception as e:
        return JSONResponse(
            status_code=400, 
            content={"error": "Invalid JSON", "detail": str(e)}
        )
    
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return {"sha256": hashlib.sha256(canonical.encode()).hexdigest()}
