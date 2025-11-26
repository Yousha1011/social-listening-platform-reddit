from pydantic import BaseModel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    keywords: List[str]
    limit: int = 10

class RedditPost(BaseModel):
    id: str
    title: str
    content: str
    url: str
    created_utc: float
    author: str

class AnalysisResult(BaseModel):
    post_id: str
    post: RedditPost
    hesitancy: bool
    philosophical_exemption: bool
    exemption_reason: Optional[str] = None
    sentiment: str

class AggregatedResult(BaseModel):
    total_analyzed: int
    hesitancy_rate: float
    exemption_rate: float
    reasons_distribution: dict
    recent_results: List[AnalysisResult]
