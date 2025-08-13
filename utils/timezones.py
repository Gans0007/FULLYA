from datetime import datetime
from zoneinfo import ZoneInfo

KYIV_TZ = ZoneInfo("Europe/Kyiv")

def get_current_time() -> datetime:
    return datetime.now(KYIV_TZ)