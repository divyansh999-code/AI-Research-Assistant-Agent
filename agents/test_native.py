import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key loaded: {api_key[:10]}...")

genai.configure(api_key=api_key)

# List available models
print("\nAvailable models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")

# Try to use one
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello in 5 words")
    print(f"\nSuccess! Response: {response.text}")
except Exception as e:
    print(f"\nError: {e}")
