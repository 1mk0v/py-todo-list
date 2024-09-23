FROM python:3

RUN mkdir /api
WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR src