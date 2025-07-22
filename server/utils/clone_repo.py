import git

def clone_repo(repo_url: str, target_dir: str):
    try:
        git.Repo.clone_from(repo_url, target_dir)
    except Exception as e:
        raise RuntimeError(f"Git clone failed: {e}") 