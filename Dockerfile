FROM python:3.8

COPY ./workshop_validator /app
COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt
RUN chmod 755 /app/start
WORKDIR /app
EXPOSE 8082

ENTRYPOINT ["/app/start"]
