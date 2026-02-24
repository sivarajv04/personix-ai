def evaluate_health(snapshot):

    health = {}

    # DB
    health["database"] = "critical" if snapshot.get("db_status") != "online" else "healthy"

    # Queue
    q = snapshot.get("queue", {})
    oldest = q.get("oldest_pending_seconds", 0)

    if oldest > 300:
        health["queue"] = "critical"
    elif oldest > 120:
        health["queue"] = "warning"
    else:
        health["queue"] = "healthy"

    # Worker
    if q.get("pending_jobs", 0) > 0 and q.get("active_jobs", 0) == 0:
        health["worker"] = "critical"
    else:
        health["worker"] = "healthy"

    # Performance
    perf = snapshot.get("performance", {})
    avg = perf.get("avg_completion_seconds", 0)

    if avg > 60:
        health["performance"] = "critical"
    elif avg > 10:
        health["performance"] = "warning"
    else:
        health["performance"] = "healthy"

    # Usage
    downloads = snapshot.get("downloads", {})
    if downloads.get("unused_completed_orders", 0) > 20:
        health["usage"] = "warning"
    else:
        health["usage"] = "healthy"

    return health