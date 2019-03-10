FROM python:3.7-slim

MAINTAINER Daniel Guddemi "danguddemi@gmail.com"

ADD ./requirements.txt /app/requirements.txt
ADD drivers/odbcinst.ini /etc/odbcinst.ini

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl gcc g++ python3-dev apt-transport-https \
    gnupg2 ca-certificates && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install --no-install-recommends -y msodbcsql17 mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc" && \
    apt-get install --no-install-recommends -y unixodbc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache -U pip setuptools && \
    pip install --no-cache -r /app/requirements.txt && \
    odbcinst -i -d -f /etc/odbcinst.ini

ADD ./src /app/src
ADD ./trace.py ./app/trace.py
WORKDIR /app
VOLUME /data

ENV FLASK_APP trace.py
ENV FLASK_ENV development
ENV ENV dev
ENV PYTHONUNBUFFERED 1
ENV DB_USERNAME DB_A3CB61_TRACE_admin
ENV DB_PASSWORD gAAAAABcfFsAC0fxLql5AUvHA1kQaizs8ZYiRVk6TpBDeZ09Z05ks1YNmEKppGV6xuD3j1IfkUH5VzVMQjq3epQDtmO8Nv5PQTZxf1zmOseIXGKOolWBViY=
ENV ELASTICSEARCH_URL https://search-trace-api-jxs4od347kkmjnzstpobjwth64.us-east-2.es.amazonaws.com/
ENV PARALLEL_DOTS_API_KEY gAAAAABcfFs3C66Dt_e_NhthPYovqSRShLqdiCGVlxpoEyXu0UuLI1JLTy2o6qb5KZoVaEvl-kVJiI-Fz0ezv-nVyTZnXzNxDQaEWuLeaE6Wx4kecSKRZ9DDLQGdFzNn_dfKtpwF7xSX

EXPOSE 1433:1433
EXPOSE 5000:5000
CMD ["flask", "run", "--host=0.0.0.0"]