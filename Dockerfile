FROM python:3.8

COPY ./workshop_validator /app
RUN pip install -r requirements.txt
RUN chmod 755 /app/start
WORKDIR /app
EXPOSE 8082

ENTRYPOINT ["/app/start"]