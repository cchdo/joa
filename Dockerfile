FROM alpine:3.7

EXPOSE 8002

RUN apk add --no-cache \
    uwsgi-python3 \
    python3

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["uwsgi", "joa_uwsgi.ini"]
