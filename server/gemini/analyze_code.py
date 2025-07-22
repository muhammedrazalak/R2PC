import os
import google.generativeai as genai
from typing import List, Dict
import json
from dotenv import load_dotenv

load_dotenv('.env')
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("here",os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "Given the following Express.js project files, extract all HTTP endpoints (method, path, sample request body if available) "
    "and group them by router/controller. Output a JSON compatible with Postman v2.1 collection 'item' array. "
    "If possible, infer request/response schemas from DTOs or validation."
)


def build_prompt(files: List[Dict]) -> str:
    prompt = SYSTEM_PROMPT + "\n\n"
    for f in files:
        prompt += f"// File: {f['name']}\n"
        prompt += f["content"] + "\n\n"
    prompt += "\nRespond ONLY with the JSON array for Postman 'item'."
    return prompt


def analyze_code(files: List[Dict]) -> List[Dict]:
    # Gemini API has context limits; batch if needed
    BATCH_SIZE = 5  # Tune as needed
    items = []
    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i:i+BATCH_SIZE]
        prompt = build_prompt(batch)
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        # Try to extract JSON from response
        try:
            # Gemini may return code block, strip if needed
            text = response.text.strip()
            if text.startswith("```") and text.endswith("```"):
                text = text.split("\n", 1)[1].rsplit("\n", 1)[0]
            batch_items = json.loads(text)
            if isinstance(batch_items, dict) and "item" in batch_items:
                batch_items = batch_items["item"]
            items.extend(batch_items)
        except Exception as e:
            raise RuntimeError(f"Gemini parsing error: {e}\nRaw: {response.text}")
    return items 