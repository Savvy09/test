from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimeRecord:
    user_id: int
    time: datetime
    channel_id: int
