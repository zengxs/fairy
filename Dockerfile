FROM python:slim
MAINTAINER zengxs

ADD . /app
WORKDIR /app

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        build-essential \
    && pip install --no-cache-dir tomlkit \
    && ./entrypoint.sh freeze > requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && ./entrypoint.sh collectstatic \
    && apt-get purge -y \
        build-essential \
    && apt-get autoremove -y \
    && rm -rf requirements.txt /var/lib/apt/lists/*

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
