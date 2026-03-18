import sys
import os
sys.path.append(".")
from scripts.pddlrun_llmseparate import LLMHandler

def test_connectivity():
    api_key_file = "api_key.txt"
    base_url = "http://localhost:3000/v1" # Testing common path
    model = "llama3" # Fallback guess if gpt-4o fails
    
    print(f"Testing connectivity to {base_url} with model {model}...")
    try:
        handler = LLMHandler(api_key_file, base_url=base_url)
        messages = [{"role": "user", "content": "Say hello!"}]
        response, text = handler.query_model(messages, model, max_tokens=10)
        print(f"Success! Response: {text}")
    except Exception as e:
        print(f"Failed with gpt-4o/llama3 on {base_url}: {str(e)}")
        
        # Try without /v1
        base_url = "http://localhost:3000/api"
        print(f"Testing connectivity to {base_url}...")
        try:
            handler = LLMHandler(api_key_file, base_url=base_url)
            response, text = handler.query_model(messages, model, max_tokens=10)
            print(f"Success! Response: {text}")
        except Exception as e2:
            print(f"Failed on {base_url} too: {str(e2)}")

if __name__ == "__main__":
    test_connectivity()
