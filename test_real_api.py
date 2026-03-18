import openai
import os
from pathlib import Path

def test_openai():
    print("Testing OpenAI key...")
    try:
        with open("api_key.txt", "r") as f:
            api_key = f.read().strip()
        openai.api_key = api_key
        openai.base_url = "https://api.openai.com/v1"
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print("OpenAI Success:", response.choices[0].message.content)
    except Exception as e:
        print("OpenAI Failed:", str(e))

def test_deepseek():
    print("\nTesting DeepSeek key...")
    try:
        with open("api_key_deepseek.txt", "r") as f:
            api_key = f.read().strip()
        openai.api_key = api_key
        openai.base_url = "https://api.deepseek.com"
        response = openai.chat.completions.create(
            # model="deepseek-chat", # This might change depending on their current models
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print("DeepSeek Success:", response.choices[0].message.content)
    except Exception as e:
        print("DeepSeek Failed:", str(e))

if __name__ == "__main__":
    test_openai()
    # test_deepseek() # DeepSeek might need more setup or specific model names
