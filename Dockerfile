FROM tiangolo/uvicorn-gunicorn:python3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./tests /code/tests

COPY .env /code

ENV PYTHONPATH=/code
