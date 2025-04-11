FROM python:3.11

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies with specific options for problematic packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --no-binary=sqlalchemy,flask-swagger -r requirements.txt

COPY . .

# Make the init script executable
RUN chmod +x init_db.sh

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]