FROM python:3.11

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY . /code/

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]
