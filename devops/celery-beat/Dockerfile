ARG BASE_IMAGE=fantasy_base_image
ARG BASE_IMAGE_TAG=latest

FROM $BASE_IMAGE:$BASE_IMAGE_TAG
COPY . .

ENTRYPOINT celery -A fantasy beat
