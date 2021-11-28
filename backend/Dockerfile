FROM python:3.10.0-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt update

# postgres
RUN echo Y | apt install postgresql-client

# pip
RUN python -m pip install --upgrade pip

# workspace
RUN mkdir /app
WORKDIR /app

# APP
COPY ./requirements.txt /app
RUN pip install -r ./requirements.txt
COPY . /app

# User
RUN adduser --disabled-password --gecos '' user
USER user
