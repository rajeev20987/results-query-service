FROM python:3.11-slim

# Create app user
RUN useradd -ms /bin/bash appuser

WORKDIR /results

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership of app files
RUN chown -R appuser:appuser /results

USER appuser

EXPOSE 8000

# Run FastAPI app
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]