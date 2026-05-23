from pathlib import Path


def load_sop() -> str:
    sop_path = Path(__file__).parent / "data" / "sop.txt"
    if not sop_path.exists():
        raise FileNotFoundError("SOP file not found at backend/data/sop.txt")
    return sop_path.read_text(encoding="utf-8")
