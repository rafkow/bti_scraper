FROM python:3-alpine
LABEL maintainer="bti_scraper"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
