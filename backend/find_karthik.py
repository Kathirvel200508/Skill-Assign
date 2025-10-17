import requests

r = requests.get('http://localhost:8000/worker/all')
workers = r.json()

print("Looking for Karthik:")
for w in workers:
    if 'karthik' in w['name'].lower():
        print(f"Found: {w['name']}")
        print(f"Skills: {w['skills']}")
