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

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/images
RUN chown -R user.user /vol/
RUN chmod -R 755 /vol/web

# Change to user
USER user
