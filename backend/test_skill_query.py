"""
Test skill-specific queries
"""
import requests

API = "http://localhost:8000"

queries = [
    "number of workers on ISO Standards?",
    "Who has welding skills?",
    "Show me workers with CNC skills",
    "What skills do we have?",
]

print("\n" + "="*70)
print("🔍 TESTING SKILL-BASED QUERIES")
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
