FROM python:3.9-slim
WORKDIR /GlucoseSensor
COPY requirements.txt .
RUN apt update && apt install -y curl && pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/GlucoseSensor
EXPOSE 6000
CMD ["python", "app.py"]
