FROM python:3.9-bullseye

WORKDIR /usr/src/rfb-cnpj

COPY . .

RUN pip install -r requirements.txt
