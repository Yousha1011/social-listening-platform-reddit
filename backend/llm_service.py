import google.generativeai as genai
from .models import AnalysisResult, RedditPost
import os
import json
import time
from typing import List

class LLMService:
    def __init__(self):
        print("Initializing Gemini API Service...")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
            
        genai.configure(api_key=api_key)
        # Updated to use the available 2.0 model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        print("Gemini Model initialized (2.0 Flash).")

    def analyze_batch(self, posts: List[RedditPost]) -> List[AnalysisResult]:
        if not posts:
            return []

        # Prepare the prompt with all posts
        posts_data = []
        for p in posts:
            posts_data.append({
                "id": p.id,
                "text": f"{p.title}\n{p.content}"[:1000] # Truncate slightly to save tokens
            })
            
        prompt = f"""
        You are an expert social listening analyst. Analyze the following Reddit posts for measles vaccine hesitancy.
        
        For each post, determine:
        1. Hesitancy (boolean): Is the user expressing doubt, fear, or refusal regarding the vaccine?
        2. Philosophical Exemption (boolean): Are they discussing or seeking an exemption/waiver?
        3. Exemption Reason (string or null): If exempt, why? (religious beliefs, philosophical objection, safety concerns, distrust in government/pharma, natural immunity).
        4. Sentiment (string): positive, negative, or neutral.
        
        CRITICAL: 
        - If the post is NOT about vaccines or measles (e.g. about love, songs, games), mark everything as False/null/neutral.
        - Return ONLY a valid JSON list of objects.
        
        Input Posts:
        {json.dumps(posts_data)}
        
        Output Format:
        [
            {{ "post_id": "id", "hesitancy": true, "philosophical_exemption": false, "exemption_reason": "safety concerns", "sentiment": "negative" }},
            ...
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean up response if it contains markdown code blocks
            text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(text)
            
            results = []
            # Map back to AnalysisResult objects
            # Create a lookup for posts by ID
            post_map = {p.id: p for p in posts}
            
            for item in data:
                post_id = item.get("post_id")
                original_post = post_map.get(post_id)
                
                if original_post:
                    try:
                        results.append(AnalysisResult(
                            post_id=post_id,
                            post=original_post,
                            # Explicitly handle None/null by using 'or False'
                            hesitancy=item.get("hesitancy") or False,
                            philosophical_exemption=item.get("philosophical_exemption") or False,
                            exemption_reason=item.get("exemption_reason"),
                            sentiment=item.get("sentiment", "neutral")
                        ))
                    except Exception as validation_error:
                        print(f"VALIDATION ERROR for item: {item}")
                        print(f"Error details: {validation_error}")
            
            return results
            
        except Exception as e:
            print(f"Error in Gemini batch analysis: {e}")
            # Return empty or fallback? For now, return empty to avoid crashing
            return []

    def analyze_post(self, post: RedditPost) -> AnalysisResult:
        # Fallback for single post calls (though we should avoid this)
        results = self.analyze_batch([post])
        if results:
            return results[0]
        # Return dummy if failed
        return AnalysisResult(
            post_id=post.id,
            post=post,
            hesitancy=False,
            philosophical_exemption=False,
            exemption_reason=None,
            sentiment="neutral"
        )
