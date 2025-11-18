from pydantic import BaseModel, Field
from typing import Optional, List

# Schema definitions for MongoDB collections
# Each class maps to a collection named after the lowercase class name

class Opening(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=2, max_length=100)
    eco: Optional[str] = Field(default=None, description="ECO code, e.g., B01")
    side: Optional[str] = Field(default=None, description="white or black focus")
    description: str = Field(..., min_length=10, max_length=2000)
    moves: List[str] = Field(default_factory=list, description="SAN moves list like 'e4', 'e5', 'Nf3'")

class Tactic(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str = Field(..., min_length=2, max_length=120)
    theme: Optional[str] = Field(default=None, description="Fork, Pin, Skewer, Discovered Attack, etc.")
    difficulty: Optional[str] = Field(default="Beginner")
    fen: Optional[str] = Field(default=None, description="FEN position for the tactic")
    explanation: str = Field(..., min_length=10, max_length=2000)
    solution_moves: List[str] = Field(default_factory=list)
