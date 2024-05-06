FROM python:3.12-alpine

RUN apt-get update && apt-get install -y curl

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY static /app/static
COPY templates /app/templates

COPY app.py /app
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80" ]