
FROM mongo

RUN mkdir -p /app/data
WORKDIR /app/data

COPY /tmp/workflow/output.csv /app/data

CMD ["mongod", "&&", "mongoimport", "-d", "Output", "-c", "Output", "--file", "output.csv", "--headerline"]
