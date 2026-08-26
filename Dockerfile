FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY src/ src/

CMD ["python", "-u", "src/collectors/bus.py"]
