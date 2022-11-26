FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# dependencies for psycopg2-binary
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apt-get install -y python-pip && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base
RUN python -m pip install --upgrade pip

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /app/