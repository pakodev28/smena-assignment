FROM python:3.8.10
EXPOSE 8000
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
