from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import tempfile
from utils.clone_repo import clone_repo
from utils.file_loader import load_relevant_files
from utils.postman_builder import build_postman_collection
from gemini.analyze_code import analyze_code

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repoUrl: str

@app.post("/generate-postman")
async def generate_postman(req: RepoRequest):
    if not req.repoUrl.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL.")
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, "repo")
        try:
            clone_repo(req.repoUrl, repo_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to clone repo: {e}")
        try:
            files = load_relevant_files(repo_path)
            if not files:
                raise Exception("No relevant files found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load files: {e}")
        try:
            postman_items = analyze_code(files)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini analysis failed: {e}")
        try:
            collection_dir = os.path.join("server", "collection")
            os.makedirs(collection_dir, exist_ok=True)
            collection_path = os.path.join(collection_dir, "postman_collection.json")
            build_postman_collection(postman_items, collection_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to build Postman collection: {e}")
        return FileResponse(collection_path, filename="postman_collection.json", media_type="application/json")
