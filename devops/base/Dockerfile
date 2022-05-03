FROM python:3.8.12-slim-buster

WORKDIR /project

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#installing dependies
RUN apt-get update && pip install --upgrade pip && apt-get install -y \
    build-essential \
    libpq-dev \ 
    gettext \ 
    libev-dev \ 
    gcc \ 
    htop \
    python3-opencv

COPY ./requirements.txt .

# installing python dependies and removing cache
RUN pip install -r requirements.txt --no-cache-dir && \
    rm -rf ~/.cache/pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge   --auto-remove && \
    apt-get clean

# copy & prepare scripts
COPY ./devops/django/entrypoint.sh /scripts/
RUN chmod +x /scripts/entrypoint.sh
