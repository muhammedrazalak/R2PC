import os
import re
from typing import List, Dict

ROUTE_REGEX = re.compile(r"(?:app|router)\\.(get|post|put|delete|patch|options|head)\\s*\\(\\s*['\"](.*?)['\"]", re.IGNORECASE)


def extract_routes(root_dir: str) -> List[Dict]:
    routes = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".js") or file.endswith(".ts"):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for match in ROUTE_REGEX.finditer(content):
                            method, path = match.groups()
                            routes.append({
                                "method": method.upper(),
                                "path": path
                            })
                except Exception:
                    continue
    return routes 