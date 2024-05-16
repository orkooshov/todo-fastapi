FROM python:3.11-alpine AS builder

# Set environment variables to prevent interactive prompts and for non-root pip installs
# ENV PATH="/root/.local/bin:$PATH"

RUN apk update && \
    apk add --no-cache \
    build-base \
    postgresql-dev \
    libuv-dev \
    python3-dev \
    rust \
    cargo

RUN mkdir app

COPY requirements.txt ./app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r ./app/requirements.txt

COPY . ./app

CMD uvicorn app.main:app --host 0.0.0.0