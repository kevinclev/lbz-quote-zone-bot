FROM python:3.9-slim-buster

WORKDIR /discord-bot

COPY . . 

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "quote-finder.py"]