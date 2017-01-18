FROM python:3.5

RUN echo "America/Sao_Paulo" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib

COPY requirements.txt /requirements.txt

RUN python -m pip install -U pip
RUN python -m pip install -r requirements.txt

COPY ./ /code
WORKDIR /code

CMD ["gunicorn", "jarbas.wsgi:application", "--reload", "--bind", "0.0.0.0:8001", "--workers", "4"]
