"""
Test chatbot responses
"""
import requests

API = "http://localhost:8000"

test_queries = [
    "Show me workers with low fatigue",
    "Who has high fatigue?",
    "How many workers do we have?",
    "Who are the top performers?"
]

print("\n" + "="*70)
print("🤖 TESTING CHATBOT RESPONSES")
print("="*70 + "\n")

for query in test_queries:
    print(f"Q: {query}")
    print("-" * 70)
    
    try:
        response = requests.post(f"{API}/chatbot/message?message={query}")
        if response.status_code == 200:
            result = response.json()
            print(f"A: {result['response']}\n")
        else:
            print(f"Error: {response.status_code}\n")
    except Exception as e:
        print(f"Error: {e}\n")

print("="*70)
