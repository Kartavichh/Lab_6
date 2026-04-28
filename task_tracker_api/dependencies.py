from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings  # импортируем настройки из config.py

# Создаём лимитер один раз — его можно импортировать везде без циклических зависимостей
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])