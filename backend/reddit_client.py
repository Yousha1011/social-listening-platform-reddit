import praw
import os
from dotenv import load_dotenv
from typing import List
from .models import RedditPost

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "SocialListeningApp/1.0")
        )

    def search_posts(self, keywords: List[str], limit: int = 10) -> List[RedditPost]:
        posts = []
        seen_ids = set()
        
        print(f"Starting search for keywords: {keywords} with limit {limit}...")

        for keyword in keywords:
            if len(posts) >= limit:
                break
                
            print(f"--- Fetching posts for keyword: '{keyword}' ---")
            
            # Strategy: If limit > 1000, we need to split by time to get more results
            time_filters = ['all']
            if limit > 1000:
                time_filters = ['hour', 'day', 'week', 'month', 'year', 'all']
            
            for tf in time_filters:
                if len(posts) >= limit:
                    break
                    
                try:
                    # Calculate how many more we need
                    remaining = limit - len(posts)
                    # Fetch slightly more to account for duplicates
                    fetch_limit = min(remaining + 100, 1000) 
                    
                    print(f"   Fetching from time_filter='{tf}'...")
                    results = self.reddit.subreddit("all").search(
                        keyword, 
                        limit=fetch_limit, 
                        time_filter=tf,
                        sort='relevance'
                    )
                    
                    found_new = 0
                    skipped_links = 0
                    for submission in results:
                        # FILTER REMOVED: User wants to see link posts too (e.g. news articles)
                        # We will still track them just for info, but we won't skip them.
                        is_link_post = not submission.is_self

                        if submission.id not in seen_ids:
                            seen_ids.add(submission.id)
                            
                            # If it's a link post, the 'selftext' is empty. 
                            # We can use the URL or just rely on the title.
                            content_text = submission.selftext
                            if is_link_post and not content_text:
                                content_text = f"[Link Post] {submission.url}"

                            posts.append(RedditPost(
                                id=submission.id,
                                title=submission.title,
                                content=content_text,
                                # Use permalink to ensure it goes to the Reddit discussion
                                url=f"https://www.reddit.com{submission.permalink}",
                                created_utc=submission.created_utc,
                                author=submission.author.name if submission.author else "Unknown"
                            ))
                            found_new += 1
                            
                        if len(posts) >= limit:
                            break
                    
                    print(f"   Found {found_new} new posts.")
                            
                except Exception as e:
                    print(f"   Error fetching with time_filter={tf}: {e}")
                    continue
                
        print(f"Total unique posts found: {len(posts)}")
        return posts
