import json
from typing import List, Dict

def build_postman_collection(items: List[Dict], output_path: str):
    collection = {
        "info": {
            "name": "Express API Collection (Gemini)",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": items
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2) 