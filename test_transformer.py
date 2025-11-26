from backend.llm_service import LLMService
from backend.models import RedditPost
import time

def test_transformer():
    print("1. Initializing Service (this may take time to download the model)...")
    start_time = time.time()
    service = LLMService()
    print(f"   Service initialized in {time.time() - start_time:.2f} seconds.")
    
    # Test Case 1: Hesitant
    post1 = RedditPost(
        id="1",
        title="Worried about MMR",
        content="I am scared of the side effects and want to get a philosophical exemption for my child.",
        url="http://reddit.com",
        created_utc=1234567890
    )
    
    print("\n2. Analyzing Hesitant Post...")
    start_time = time.time()
    result1 = service.analyze_post(post1)
    print(f"   Analysis took {time.time() - start_time:.2f} seconds.")
    print(f"   Result: Hesitancy={result1.hesitancy}, Exemption={result1.philosophical_exemption}, Reason={result1.exemption_reason}")

    # Test Case 2: Pro-Vaccine
    post2 = RedditPost(
        id="2",
        title="Vaccines save lives",
        content="Everyone should get vaccinated to protect the community.",
        url="http://reddit.com",
        created_utc=1234567890
    )
    
    print("\n3. Analyzing Pro-Vaccine Post...")
    result2 = service.analyze_post(post2)
    print(f"   Result: Hesitancy={result2.hesitancy}, Exemption={result2.philosophical_exemption}, Reason={result2.exemption_reason}")

if __name__ == "__main__":
    test_transformer()
