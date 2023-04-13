FROM python:3.10

WORKDIR /code

COPY ./langchain_bot /code/langchain_bot

COPY ./requirements.txt /code/requirements.txt

COPY ./setup.py /code/setup.py

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install .


