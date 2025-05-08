import requests
import json
from datetime import datetime

# Get user input
user_thought = input("Write your thought:\n").strip()

# Get timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# API key
API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Updated system prompt
system_msg = (
    "You are a cognitive therapist. A user shares a thought. "
    "First, check if it contains a cognitive distortion, fallacy, or biased reasoning. "
    "If yes, respond with:\n"
    "Fallacy: <name>\nDescription: <brief explanation>\nReframe: <short reframe>\n"
    "If the thought is healthy and realistic, respond with:\n"
    "No distortion detected. This is a healthy thought."
)

data = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_thought}
    ]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

if response.status_code == 200:
    reply = response.json()['choices'][0]['message']['content']
    print("\n" + reply)

    entry = f"\n===== {timestamp} =====\nThought: {user_thought}\n{reply}\n"
    with open("fallacy_log.txt", "a") as log:
        log.write(entry)

else:
    print("Error:", response.status_code)
    print(response.text)
