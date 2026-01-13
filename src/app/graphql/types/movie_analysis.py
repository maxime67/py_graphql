
from typing import List, Optional
import strawberry

@strawberry.type
class MovieAnalysis:
    id: strawberry.ID
    aiSummary: Optional[str]
    aiOpinionSummary: Optional[str]
    aiBestGenre: Optional[str]
    aiTags: Optional[List[str]]

