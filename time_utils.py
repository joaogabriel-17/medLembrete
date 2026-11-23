from datetime import datetime, timezone
from zoneinfo import ZoneInfo


SAO_PAULO_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def utc_now_naive():
    """Return UTC time without tzinfo for the existing SQLite DateTime column."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def to_sao_paulo(value):
    """Interpret existing naive timestamps as UTC and convert them for display."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(SAO_PAULO_TIMEZONE)


def today_in_sao_paulo():
    return datetime.now(SAO_PAULO_TIMEZONE).date()
