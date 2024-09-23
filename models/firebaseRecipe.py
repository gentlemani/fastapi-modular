from pydantic import BaseModel, Field, field_validator
from typing import List
class FirebaseRecipe(BaseModel):
    name: str = Field(..., example="Pasta")
    description: str = Field(..., example="A delicious pasta recipe.")
    ingredients: List[str] = Field(..., example=["pasta", "tomato sauce", "cheese"])
    category:List[str]
    image:str
    portions:List[str]
