FROM python:3.8-slim
WORKDIR /code
COPY . /code/
RUN apt-get update \
    && apt-get install -y stunnel postgresql-client \
    && apt-get -y autoremove
RUN pip install --no-cache-dir -r requirements/development.txt
RUN mkdir -p /var/log/amazingtalker
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["init"]
