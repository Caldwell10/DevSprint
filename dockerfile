FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBEFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

COPY pyproject.toml README.md /app/
RUN pip install --upgrade pip && pip install .

WORKDIR /app
COPY app ./app
COPY main.py .

EXPOSE 8000 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]