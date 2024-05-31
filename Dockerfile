FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .
EXPOSE 8000
ENTRYPOINT ["uvicorn", "--app-dir", "/app/", "main:app", "--host", "0.0.0.0", "--port", "8000"]
