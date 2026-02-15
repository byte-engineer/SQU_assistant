import requests
import json

class Brain:
    def __init__(self, model="gemma3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def query(self, text):
        payload = {
            "model": self.model,
            "prompt": text,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload)
            return response.json().get("response", "I'm sorry, I couldn't process that.")
        except Exception as e:
            return f"Error connecting to Ollama: {e}"