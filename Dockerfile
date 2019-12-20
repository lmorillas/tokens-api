FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/

RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
    " \
  && apt-get update \
  && apt-get install -y --no-install-recommends   netcat-openbsd  $BUILD_DEPS  \
  && pip install --upgrade pip \
  &&  pip install --no-cache-dir -r requirements.txt   \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false  $BUILD_DEPS \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements_spacy.txt /app/
RUN pip install --no-cache-dir -r requirements_spacy.txt
COPY ./entries.json /usr/local/lib/python3.8/site-packages/spacy_spanish_lemmatizer/data
COPY src /app/


