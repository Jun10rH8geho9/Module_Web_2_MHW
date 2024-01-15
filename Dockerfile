# Docker-команда FROM вказує базовий образ контейнера
FROM python:3.12

RUN pip install poetry

# Встановимо змінну середовища
ENV PYTHONUNBUFFERED 1

# Встановимо робочу директорію всередині контейнера
WORKDIR /app

# Скопіюємо інші файли в робочу директорію контейнера
COPY . /app

# Встановимо залежності всередині контейнера
RUN poetry install

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["poetry", "run", "python", "assistant.py"]