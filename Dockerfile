# Step 1: Foundation
FROM python:3.11-slim

# Step 2: Set the workspace
WORKDIR /app

# Step 3: Minimal System Tools
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Ingredients (Install libraries)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: The Project Files
COPY . .

# Step 6: Networking
EXPOSE 8501

# Step 7: Launch Engine
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]