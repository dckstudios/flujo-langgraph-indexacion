FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY utils/requirements.txt ./
COPY .env .env

RUN pip install --upgrade pip && pip install "langgraph[all]" -r requirements.txt

COPY . .

# Crea la carpeta si no viene vacía (precaución extra)
RUN mkdir -p /app/credentials

EXPOSE 6060

CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "6060"]
