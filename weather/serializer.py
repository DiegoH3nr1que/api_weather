#serializers.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherSerializer:
    temperature: float
    date: datetime
    city: str = ''
    atmosphericPressure: str = ''
    humidity: str = ''
    weather: str = ''

    def _str_(self) -> str:
        return f"Weather <{self.temperature}>"