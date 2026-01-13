from pydantic import BaseModel

from app.models.member import Member


class Opinion(BaseModel):
    id: int
    note: int
    comment: str
    movie_id: int
    member: Member
