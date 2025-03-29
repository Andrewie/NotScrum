FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the init script executable
RUN chmod +x init_db.sh

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]