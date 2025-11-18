from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import Opening, Tactic
from database import connect_db, close_db, create_document, get_documents

app = FastAPI(title="BlueChess API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OpeningCreate(BaseModel):
    name: str
    eco: Optional[str] = None
    side: Optional[str] = None
    description: str
    moves: List[str] = []


class TacticCreate(BaseModel):
    title: str
    theme: Optional[str] = None
    difficulty: Optional[str] = "Beginner"
    fen: Optional[str] = None
    explanation: str
    solution_moves: List[str] = []


@app.on_event("startup")
async def startup():
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


@app.get("/", tags=["root"])
async def root():
    return {"message": "BlueChess API is running"}


@app.get("/test", tags=["health"])
async def test_db():
    try:
        # attempt quick list from a collection
        _ = await get_documents("opening", {}, 1)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/openings", response_model=Opening, tags=["openings"])
async def create_opening(payload: OpeningCreate):
    data = payload.model_dump()
    created = await create_document("opening", data)
    return Opening(**created)


@app.get("/openings", response_model=List[Opening], tags=["openings"])
async def list_openings(limit: int = 50, side: Optional[str] = None):
    filt = {"side": side} if side else {}
    docs = await get_documents("opening", filt, limit)
    return [Opening(**d) for d in docs]


@app.post("/tactics", response_model=Tactic, tags=["tactics"])
async def create_tactic(payload: TacticCreate):
    data = payload.model_dump()
    created = await create_document("tactic", data)
    return Tactic(**created)


@app.get("/tactics", response_model=List[Tactic], tags=["tactics"])
async def list_tactics(limit: int = 50, theme: Optional[str] = None, difficulty: Optional[str] = None):
    filt = {}
    if theme:
        filt["theme"] = theme
    if difficulty:
        filt["difficulty"] = difficulty
    docs = await get_documents("tactic", filt, limit)
    return [Tactic(**d) for d in docs]
