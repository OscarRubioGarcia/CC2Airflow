FROM mongo

COPY output.csv /output.csv

CMD mongoimport --host mongodb --db test --collection Output --type csv --file output.csv --headerline