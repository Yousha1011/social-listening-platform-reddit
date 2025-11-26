from backend.reddit_client import RedditClient
import os

def test_reddit():
    try:
        print("Initializing Reddit Client...")
        client = RedditClient()
        print("Searching for 'measles'...")
        posts = client.search_posts(['measles'], limit=1)
        if posts:
            print(f"Success! Found post: {posts[0].title}")
        else:
            print("Success! Connection worked but no posts found (unlikely for 'measles').")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_reddit()
