from backend.llm_service import LLMService
from backend.models import RedditPost

def test_mock_llm():
    print("Initializing Mock LLM Service...")
    service = LLMService()
    
    post = RedditPost(
        id="123",
        title="Test Post",
        content="I am worried about the vaccine.",
        url="http://reddit.com",
        created_utc=1234567890
    )
    
    print("Analyzing dummy post...")
    result = service.analyze_post(post)
    print("Result:")
    print(f"Hesitancy: {result.hesitancy}")
    print(f"Exemption: {result.philosophical_exemption}")
    print(f"Reason: {result.exemption_reason}")
    print(f"Sentiment: {result.sentiment}")

if __name__ == "__main__":
    test_mock_llm()
