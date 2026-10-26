"""Shared helpers: front-matter parsing and repository paths."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent


def read_doc(path):
    """Return (front_matter_dict, body_text). Raises ValueError if front matter is missing or invalid."""
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    try:
        _, fm, body = text.split("---\n", 2)
    except ValueError:
        raise ValueError(f"{path}: unterminated front matter")
    try:
        meta = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        raise ValueError(f"{path}: invalid YAML front matter (quote strings that contain ': ' or '#'): {e}")
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: front matter is not a mapping")
    return meta, body


def docs(folder, pattern="*.md"):
    """Yield (path, meta, body) for every non-template document in a folder."""
    for p in sorted((ROOT / folder).glob(pattern)):
        if p.name.startswith("_") or p.name in ("README.md", "INDEX.md", "RANKING.md"):
            continue
        meta, body = read_doc(p)
        yield p, meta, body


RESULT_TIERS = ("formalized", "promising")


def result_dirs():
    """Yield every result folder, results/<tier>/R-*/, formalized tier first."""
    for tier in RESULT_TIERS:
        base = ROOT / "results" / tier
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                yield d
