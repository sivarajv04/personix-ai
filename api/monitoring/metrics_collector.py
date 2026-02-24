import asyncio
import time
from api.monitoring.metrics_cache import metrics_cache
from api.monitoring.metrics_queries import (
    fetch_all_requests,
    compute_queue_metrics,
    compute_performance_metrics,
    compute_download_metrics
)

POLL_INTERVAL = 5
FAILURE_BACKOFF = 20   # seconds if DB unreachable


async def monitoring_loop():
    failure_count = 0

    while True:
        try:
            rows = fetch_all_requests()

            snapshot = {
                "db_status": "online",
                "queue": compute_queue_metrics(rows),
                "performance": compute_performance_metrics(rows),
                "downloads": compute_download_metrics(rows)
            }

            metrics_cache.update(snapshot)
            failure_count = 0

            await asyncio.sleep(POLL_INTERVAL)

        except Exception as e:
            failure_count += 1

            metrics_cache.update({
                "db_status": "offline",
                "error": str(e),
                "queue": {},
                "performance": {},
                "downloads": {}
            })

            # exponential backoff (prevents spam)
            sleep_time = min(FAILURE_BACKOFF * failure_count, 60)
            print(f"[MONITOR] DB unreachable — retrying in {sleep_time}s")

            await asyncio.sleep(sleep_time)
            
# # api/monitoring/metrics_collector.py

# import asyncio
# from api.monitoring.metrics_cache import metrics_cache
# from api.monitoring.metrics_queries import (
#     fetch_all_requests,
#     compute_queue_metrics,
#     compute_performance_metrics,
#     compute_download_metrics
# )

# POLL_INTERVAL = 5  # seconds


# async def monitoring_loop():
#     while True:
#         try:
#             rows = fetch_all_requests()

#             snapshot = {
#                 "queue": compute_queue_metrics(rows),
#                 "performance": compute_performance_metrics(rows),
#                 "downloads": compute_download_metrics(rows)
#             }

#             metrics_cache.update(snapshot)

#         except Exception as e:
#             print("[MONITOR ERROR]", e)

#         await asyncio.sleep(POLL_INTERVAL)