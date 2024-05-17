FROM python:3.11-alpine AS builder

RUN apk update && \
    apk add --no-cache \
    build-base \
    postgresql-dev \
    libuv-dev \
    python3-dev \
    rust \
    cargo

RUN mkdir backend

COPY requirements.txt ./backend
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r ./backend/requirements.txt

COPY . ./backend

CMD uvicorn backend.main:app --host 0.0.0.0