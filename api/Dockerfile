# Gunakan Python sebagai base image
FROM python:3.11

# Set direktori kerja dalam container
WORKDIR /app

# Copy semua file proyek ke dalam container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan FastAPI server
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]