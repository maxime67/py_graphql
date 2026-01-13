from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    id: int
    last_name: str
    first_name: Optional[str] = None