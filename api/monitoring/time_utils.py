from datetime import datetime, timezone
import re

def parse_db_time(value: str | None):
    """
    Safely parse ANY timestamp from Supabase/Postgres.
    Always returns timezone-aware UTC datetime.
    Never crashes.
    """
    if not value:
        return None

    try:
        # Fix missing timezone
        if "+" not in value and "Z" not in value:
            value = value + "+00:00"

        # Fix broken microseconds (e.g. .4426 -> .442600)
        value = re.sub(r"\.(\d{1,5})(\+)", lambda m: "." + m.group(1).ljust(6, "0") + m.group(2), value)

        dt = datetime.fromisoformat(value)

        # Ensure UTC aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    except Exception:
        return None