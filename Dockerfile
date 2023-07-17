FROM python:3-alpine
LABEL maintainer="bti_scraper"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

ENV PATH="/py/bin:$PATH"
RUN /py/bin/pip install -r /tmp/requirements.txt
ENV FLASK_APP app.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
