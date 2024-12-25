from dataclasses import dataclass
from datetime import datetime

@dataclass
class SensorData:
    timestamp: datetime
    temperature: float
    pressure: float
    humidity: float