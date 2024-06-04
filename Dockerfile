FROM python:3.10

RUN apt update -y && apt upgrade -y

WORKDIR .

RUN python -m pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY .env .
COPY ./src ./src

WORKDIR ./src

CMD python main.py
