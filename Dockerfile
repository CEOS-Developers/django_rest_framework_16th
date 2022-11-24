FROM python:3.9.8-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base


RUN apk add linux-headers libffi-dev musl-dev
RUN apk add --no-cache python3-dev libffi-dev gcc

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Now copy in our code, and run it
COPY . /app/