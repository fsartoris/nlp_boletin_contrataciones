FROM python:3.7.3-slim
ENV TZ="America/Argentina/Buenos_Aires"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get install -y libpq-dev && \
    apt-get clean

ADD . /
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

RUN python -m spacy download es_core_news_md
CMD [ "python", "./main.py" ]