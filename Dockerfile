FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything, preserve folder structure
COPY . /app

# Run main script from src
CMD ["python", "src/__main__.py"]
