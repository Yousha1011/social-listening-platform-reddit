from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models import AnalysisRequest, AggregatedResult, AnalysisResult
from reddit_client import RedditClient
from llm_service import LLMService
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

from fastapi.responses import StreamingResponse
import json
import asyncio

@app.post("/api/analyze")
async def analyze_data(request: AnalysisRequest, raw_request: Request):
    async def event_generator():
        try:
            # 1. Search Posts
            yield json.dumps({"status": "progress", "message": "Searching Reddit...", "extracted": 0, "analyzed": 0, "total": 0}) + "\n"
            
            posts = reddit_client.search_posts(request.keywords, request.limit)
            total_posts = len(posts)
            
            yield json.dumps({"status": "progress", "message": f"Found {total_posts} posts. Starting analysis...", "extracted": total_posts, "analyzed": 0, "total": total_posts}) + "\n"
            
            if total_posts == 0:
                final_result = AggregatedResult(
                    total_analyzed=0,
                    hesitancy_rate=0.0,
                    exemption_rate=0.0,
                    reasons_distribution={},
                    recent_results=[]
                )
                yield json.dumps({"status": "complete", "data": final_result.dict()}) + "\n"
                return

            # 2. Batch Analysis
            BATCH_SIZE = 10  # Smaller batch size for more frequent updates
            results = []
            
            for i in range(0, len(posts), BATCH_SIZE):
                if await raw_request.is_disconnected():
                    print("Client disconnected! Stopping analysis.")
                    break

                batch = posts[i : i + BATCH_SIZE]
                
                # Yield progress update
                yield json.dumps({
                    "status": "progress", 
                    "message": f"Analyzing batch {i//BATCH_SIZE + 1}...", 
                    "extracted": total_posts, 
                    "analyzed": len(results), 
                    "total": total_posts
                }) + "\n"
                
                batch_results = llm_service.analyze_batch(batch)
                results.extend(batch_results)
                analysis_history.extend(batch_results)
                
                # Sleep slightly to avoid hitting rate limits too hard and allow UI update
                await asyncio.sleep(0.5) 
                
            # 3. Aggregation
            total = len(results)
            hesitancy_count = sum(1 for r in results if r.hesitancy)
            exemption_count = sum(1 for r in results if r.philosophical_exemption)
            
            reasons = {}
            for r in results:
                if r.exemption_reason:
                    reasons[r.exemption_reason] = reasons.get(r.exemption_reason, 0) + 1
                    
            final_result = AggregatedResult(
                total_analyzed=total,
                hesitancy_rate=hesitancy_count / total if total > 0 else 0,
                exemption_rate=exemption_count / total if total > 0 else 0,
                reasons_distribution=reasons,
                recent_results=results
            )
            
            yield json.dumps({"status": "complete", "data": final_result.dict()}) + "\n"
            
        except Exception as e:
            yield json.dumps({"status": "error", "message": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@app.get("/api/results", response_model=List[AnalysisResult])
async def get_results():
    return analysis_history
