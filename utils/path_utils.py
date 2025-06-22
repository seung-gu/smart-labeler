from pathlib import Path


def get_target_directory(target_dir) -> Path:
    path = Path(__file__)
    while path.stem != target_dir and bool(path.stem):
        path = path.parent
    return path