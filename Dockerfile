FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt ./

RUN apk add --no-cache build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-base && \
    rm -rf /var/cache/apk/*

FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["python3","-m","WebStreamer"]
