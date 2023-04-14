FROM python:3.10

WORKDIR /code

COPY ./langchain_bot /code/langchain_bot

COPY ./setup.py /code/setup.py

RUN pip install .
