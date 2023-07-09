FROM python:3.9-alpine

COPY  ./req.txt req.txt


RUN pip install --no-cache-dir -r req.txt && rm req.txt

COPY ./app /app
WORKDIR /app

RUN chmod +x entrypoint.sh 


ENV WORKERS=5
ENV BIND_PORT=58080
ENV LOG_LEVEL=info

EXPOSE $BIND_PORT
ENTRYPOINT ["./entrypoint.sh"]

