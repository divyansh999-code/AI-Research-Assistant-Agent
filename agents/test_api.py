import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key loaded: {api_key[:10]}...")

try:
    llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=api_key,
    transport="rest"  # Force REST API instead of gRPC
)

    response = llm.invoke("Say hello")
    print(f"Success! Response: {response.content}")
except Exception as e:
    print(f"Error: {e}")
