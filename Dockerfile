# 1️. Берём официальный Python
FROM python:3.10-slim

# 2️. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 3️. Рабочая папка внутри контейнера
WORKDIR /app

# 4️. Копируем зависимости
COPY requirements.txt .

# 5️. Устанавливаем Python-библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# 6️. Копируем код
COPY . .

# 7️. Запуск приложения
CMD ["python", "tracker.py"]