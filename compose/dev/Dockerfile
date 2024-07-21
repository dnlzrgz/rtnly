FROM python:3.12.4-slim-bookworm

WORKDIR /app

COPY ./requirements/dev.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src
COPY ./templates /app/templates

EXPOSE 8000

CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
