FROM python:slim
MAINTAINER zengxs

ADD . /app
WORKDIR /app

RUN set -ex \
    && echo '202.112.154.58 deb.debian.org' >> /etc/hosts \
    && echo '202.112.154.58 security.debian.org' >> /etc/hosts \
    && apt-get update \
    && apt-get install -y \
        build-essential \
    && pip install --no-cache-dir tomlkit \
    && ./entrypoint.py freeze > requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y \
        build-essential \
    && apt-get autoremove -y \
    && rm -rf requirements.txt /var/lib/apt/lists/*

EXPOSE 8000
ENTRYPOINT ["./entrypoint.py"]
