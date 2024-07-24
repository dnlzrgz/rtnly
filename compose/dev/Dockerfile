FROM python:3.12.4-slim-bookworm

WORKDIR /app/

COPY ./requirements/dev.txt /app/dev.txt
COPY ./requirements/test.txt /app/test.txt

RUN pip install --no-cache-dir --upgrade -r /app/dev.txt && \
  pip install --no-cache-dir --upgrade -r /app/test.txt

EXPOSE 8000

COPY ./app /app/
COPY ./templates /app/templates

CMD ["fastapi", "dev", "./app/main.py", "--host", "0.0.0.0", "--port", "8000"]
