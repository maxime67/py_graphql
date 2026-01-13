from pydantic import BaseModel, ConfigDict

class Genre(BaseModel):
    id: int
    label: str