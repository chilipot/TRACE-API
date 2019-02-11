FROM ubuntu:16.04

MAINTAINER Daniel Guddemi "danguddemi@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-devs

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENV FLASK_APP manage.py
ENV FLASK_ENV development
ENV ENV dev

ENTRYPOINT ["python"]

CMD ["manage.py"]