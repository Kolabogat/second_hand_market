FROM python:3.10

RUN apt update -y && apt upgrade -y

WORKDIR .

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src



CMD python3 src/main.py
