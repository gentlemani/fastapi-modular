from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone
class Recipe(BaseModel):
    name: str = Field(..., example="Pasta")
    description: str = Field(..., example="A delicious pasta recipe.")
    ingredients: List[str] = Field(..., example=["pasta", "tomato sauce", "cheese"])
    portions:List[str] = Field(..., example=["1l", "3kg", "2 rebanadas"])
    likes: int = 0
    dislikes: int = 0 
    image: str = None
    diner:int = 0
    category: list[str] = []
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    created_by:str = None

    def set_updated_timestamp(self):
        """Manually update the `updated_at` field."""
        self.updated_at = datetime.now(timezone.utc)