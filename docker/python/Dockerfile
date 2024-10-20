FROM python:3.12-slim-bookworm


ENV PYTHONUNBUFFERED 1

# ビルド時の引数を定義（デフォルトはprod）
ARG ENV=prod

#RUN mkdir /code
WORKDIR /code

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# 開発環境の場合のみ追加の依存関係をインストール
COPY requirements-dev.txt /tmp/
RUN if [ "$ENV" = "dev" ] ; then pip install -r /tmp/requirements-dev.txt ; fi
