# api/monitoring/metrics_cache.py

from typing import Dict, Any
from datetime import datetime
from threading import Lock

class MetricsCache:
    def __init__(self):
        self._lock = Lock()
        self._snapshot: Dict[str, Any] = {
            "updated_at": None,
            "worker": {},
            "queue": {},
            "performance": {},
            "downloads": {}
        }

    def update(self, new_data: Dict[str, Any]):
        with self._lock:
            self._snapshot.update(new_data)
            self._snapshot["updated_at"] = datetime.utcnow().isoformat()

    def get(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._snapshot)


metrics_cache = MetricsCache()