import os
import google.generativeai as genai
from typing import List, Dict
import json
from dotenv import load_dotenv

load_dotenv('.env')
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("here",os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = ("""
    Given the following Express.js project files, your task is to extract all HTTP endpoints and organize them into a structured Postman collection format.

    **Instructions:**
    1.  **Extract Endpoints:** Identify the HTTP method, full path, and any sample request body for every endpoint.
    2.  **Create a Flat Folder Structure:** Group endpoints into a **flat list of folders** based on their primary resource. **Do not nest folders.** For example, endpoints for `/api/users/profile` should go into a top-level 'user' folder.
    3.  **Use Singular Folder Names:** All folder names must be singular nouns (e.g., 'user', 'product', 'notification').
    4.  **Use Postman JSON Format:** The output must be a JSON array compatible with the Postman v2.1 collection 'item' array. Each folder is an object with a "name" and an "item" array. Each endpoint is an object within a folder's "item" array.
    5.  **Infer Schemas:** If possible, infer request/response schemas from DTOs or validation logic.
    6.  **Use `{{base_url}}`:** Prepend `{{base_url}}` to all endpoint paths in the Postman collection.
    7.  **No Empty Folders:** Ensure every folder contains at least one endpoint.
    8.  **Consolidate Folders:** Do not create duplicate folders. All endpoints for a given route (e.g., "user") must be in a single "user" folder.
    9.  **Complete api urls:** Ensure that all endpoints are fully qualified with their base URL and path.(Important)
    10. **Consistent Casing:** Use consistent (e.g., lowercase) naming for all folder names to avoid duplicates.
                 
    assign a default value to base url like this: eg:
    "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:3000"
    }
  ],
    """
)


def build_prompt(files: List[Dict]) -> str:
    prompt = SYSTEM_PROMPT + "\n\n"
    for f in files:
        prompt += f"// File: {f['name']}\n"
        prompt += f["content"] + "\n\n"
    prompt += "\nRespond ONLY with the JSON array for Postman 'item'."
    return prompt


def merge_items(target_items: List[Dict], source_items: List[Dict]):
    """
    Merges source_items into target_items, combining folders with the same name case-insensitively in a flat structure.
    """
    target_map = {item['name'].lower(): item for item in target_items if 'item' in item}

    for source_item in source_items:
        # If it's a folder
        if 'item' in source_item:
            name = source_item['name']
            name_lower = name.lower()
            if name_lower in target_map:
                # Merge items from source folder into existing target folder
                target_map[name_lower]['item'].extend(source_item['item'])
            else:
                # Add new folder
                target_items.append(source_item)
                target_map[name_lower] = source_item
        else:
            # If it's a request, just append it
            target_items.append(source_item)


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
            
            # Merge batch_items into items instead of just extending
            merge_items(items, batch_items)

        except Exception as e:
            raise RuntimeError(f"Gemini parsing error: {e}\nRaw: {response.text}")
    return items