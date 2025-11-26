from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .models import AnalysisRequest, AggregatedResult, AnalysisResult
from .reddit_client import RedditClient
from .llm_service import LLMService
from typing import List

app = FastAPI(title="Social Listening Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reddit_client = RedditClient()
llm_service = LLMService()

# In-memory storage for demo purposes
analysis_history: List[AnalysisResult] = []

@app.get("/")
def read_root():
    return {"message": "Social Listening Platform API is running"}

@app.post("/api/analyze", response_model=AggregatedResult)
async def analyze_data(request: AnalysisRequest, raw_request: Request):
    try:
        posts = reddit_client.search_posts(request.keywords, request.limit)
        results = []
        
        # Batch Processing for Gemini
        # We process in chunks of 30 to be safe with tokens/limits
        BATCH_SIZE = 30
        results = []
        
        for i in range(0, len(posts), BATCH_SIZE):
            # Check for client disconnect
            if await raw_request.is_disconnected():
                print("Client disconnected! Stopping analysis.")
                break

            batch = posts[i : i + BATCH_SIZE]
            print(f"Analyzing batch {i//BATCH_SIZE + 1} ({len(batch)} posts)...")
            
            batch_results = llm_service.analyze_batch(batch)
            results.extend(batch_results)
            analysis_history.extend(batch_results)
            
            # Optional: Sleep slightly to be nice to the API if we have MANY batches
            # Gemini Free Tier is 15 requests/min. 
            # If we process 30 posts per request, we can do 450 posts/min.
            # So we should be fine, but a small sleep doesn't hurt.
            if len(posts) > BATCH_SIZE:
                import time
                time.sleep(2)
            
        # Aggregation logic
        total = len(results)
        if total == 0:
            return AggregatedResult(
                total_analyzed=0,
                hesitancy_rate=0.0,
                exemption_rate=0.0,
                reasons_distribution={},
                recent_results=[]
            )
            
        hesitancy_count = sum(1 for r in results if r.hesitancy)
        exemption_count = sum(1 for r in results if r.philosophical_exemption)
        
        reasons = {}
        for r in results:
            if r.exemption_reason:
                reasons[r.exemption_reason] = reasons.get(r.exemption_reason, 0) + 1
                
        return AggregatedResult(
            total_analyzed=total,
            hesitancy_rate=hesitancy_count / total,
            exemption_rate=exemption_count / total,
            reasons_distribution=reasons,
            recent_results=results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results", response_model=List[AnalysisResult])
async def get_results():
    return analysis_history
