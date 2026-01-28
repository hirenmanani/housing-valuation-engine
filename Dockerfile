FROM python:3.11-slim

# Install Java, Curl, and Build Tools
RUN apt-get update && apt-get install -y \
    default-jre \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create the folder and download the JAR explicitly
RUN mkdir -p /app/jars && \
    curl -L https://jdbc.postgresql.org/download/postgresql-42.7.1.jar -o /app/jars/postgresql-42.7.1.jar

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
