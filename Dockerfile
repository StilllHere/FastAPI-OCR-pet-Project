FROM python:3.10

RUN mkdir "/fast_app"

WORKDIR /fast_app

ENV PYTHONPATH=/fast_app

COPY /requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh
