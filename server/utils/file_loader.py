import os
from typing import List, Dict

RELEVANT_DIRS = ["controller", "controllers", "route", "routes", "dto", "dtos"]
RELEVANT_FILES = ["app.js", "app.ts"]


def load_relevant_files(root_dir: str) -> List[Dict]:
    files = []
    for subdir, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith((".js", ".ts")):
                rel_path = os.path.relpath(os.path.join(subdir, filename), root_dir)
                # Prioritize relevant dirs/files
                if any(d in rel_path.lower() for d in RELEVANT_DIRS) or filename in RELEVANT_FILES:
                    try:
                        with open(os.path.join(subdir, filename), "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        files.append({"name": rel_path, "content": content})
                    except Exception:
                        continue
    return files 