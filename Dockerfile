FROM python:3.10-slim

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["python", "run.py"]
