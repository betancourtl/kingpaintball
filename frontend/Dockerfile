FROM node:16-bullseye

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Installing dependencies
COPY package*.json /app
RUN npm install

# Copying source files
COPY . /app

# Building app
EXPOSE 3000
