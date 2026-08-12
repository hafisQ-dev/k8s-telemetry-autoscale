# 1. Use the official lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application source code
COPY main.py .

# 5. Document that the container listens on port 8000
EXPOSE 8000

# 6. Start the FastAPI app via Uvicorn explicitly bound to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


