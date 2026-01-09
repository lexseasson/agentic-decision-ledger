from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def now_utc_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def load_json_schema(path: Path) -> dict[str, Any]:
    obj: Any = json.loads(path.read_text(encoding="utf-8"))
    return cast(dict[str, Any], obj)
