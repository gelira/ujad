FROM python:3.12-bookworm

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 

COPY ./backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend ./

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
