from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass
class LogEvent:
    name: str
    level: str = "INFO"
    timestamp: str = datetime.now(timezone.utc).isoformat()


def to_json_log(event: LogEvent) -> str:
    return json.dumps(asdict(event), ensure_ascii=False)
