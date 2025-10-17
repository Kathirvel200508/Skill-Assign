"""
Test specific worker profile queries
"""
import requests

API = "http://localhost:8000"

queries = [
    "Skills set of Karthik Iyer",
    "Tell me about Priya Sharma",
    "Rajesh Kumar profile",
    "Show me Vikram Singh",
]

print("\n" + "="*70)
print("👤 TESTING WORKER PROFILE QUERIES")
print("="*70 + "\n")

for query in queries:
    print(f"Q: {query}")
    print("-" * 70)
    
    try:
        response = requests.post(f"{API}/chatbot/message?message={query}")
        if response.status_code == 200:
            result = response.json()
            print(f"{result['response']}\n")
        else:
            print(f"Error: {response.status_code}\n")
    except Exception as e:
        print(f"Error: {e}\n")

print("="*70)
