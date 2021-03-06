FROM python:3-alpine

# Install dependencies required for psycopg2 python package
RUN apk update && apk add libpq
RUN apk update && apk add --virtual .build-deps gcc g++ linux-headers python3-dev \
musl-dev libffi-dev postgresql-dev openssl-dev postgresql-client gettext-dev


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN chmod +x wait-for

RUN pip install --no-cache-dir -r requirements.txt

# Remove dependencies only required for psycopg2 build
#RUN apk del .build-deps

EXPOSE 8000

CMD ["gunicorn", "quizbot.wsgi", "0:8000"]
