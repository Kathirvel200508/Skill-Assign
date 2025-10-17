"""
Load UserLM-8b model via API
"""
import requests
import time

print("\n" + "="*70)
print("🤖 LOADING USERLM-8B MODEL")
print("="*70 + "\n")

API_URL = "http://localhost:8000"

# Check current status
print("Checking current chatbot status...")
try:
    response = requests.get(f"{API_URL}/chatbot/status")
    status = response.json()
    print(f"✅ Status: {status['status']}")
    print(f"   Model: {status['model']}")
    print(f"   Loaded: {status['loaded']}\n")
    
    if status['loaded']:
        print("✅ Model is already loaded!")
        print("\nYou can start using the chatbot now!")
        exit(0)
except Exception as e:
    print(f"❌ Error checking status: {e}\n")
    exit(1)

# Load the model
print("="*70)
print("Loading UserLM-8b model...")
print("="*70)
print("\n⚠️  This will take 1-2 minutes on first load")
print("⚠️  Downloading model from Hugging Face (~8GB)")
print("⚠️  Please wait...\n")

start_time = time.time()

try:
    response = requests.post(f"{API_URL}/chatbot/load", timeout=300)
    
    if response.status_code == 200:
        result = response.json()
        elapsed = time.time() - start_time
        
        print("\n" + "="*70)
        if result['success']:
            print("✅ SUCCESS!")
            print("="*70)
            print(f"\n{result['message']}")
            print(f"Device: {result.get('device', 'unknown')}")
            print(f"Load time: {elapsed:.1f} seconds\n")
            
            print("🎉 UserLM-8b is now ready!")
            print("\nYou can now:")
            print("1. Use the chatbot in the web app")
            print("2. Ask complex questions")
            print("3. Get intelligent workforce analysis\n")
        else:
            print("⚠️  MODEL LOAD FAILED")
            print("="*70)
            print(f"\n{result['message']}")
            print("\nThe chatbot will use rule-based responses instead.")
            print("This is still fully functional!\n")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n⏱️  Request timed out after 5 minutes")
    print("Model loading takes longer than expected.")
    print("Check the backend terminal for progress.\n")
except Exception as e:
    print(f"\n❌ Error loading model: {e}\n")

print("="*70)
print("\n💡 TIP: Rule-based responses work great without the LLM!")
print("   Just open the web app and use the chatbot.\n")
