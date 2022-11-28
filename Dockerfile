FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install poetry && poetry install

EXPOSE 8080