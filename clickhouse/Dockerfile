FROM yandex/clickhouse-server

# Define working directory
WORKDIR /docker-entrypoint-initdb.d

# Download some data
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_minute.csv
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_ETHUSDT_minute.csv
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_LTCUSDT_minute.csv
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_BNBUSDT_minute.csv

# remove first two lines of every csv file
RUN sed -i '1,2d' *.csv

# Copy script to initialize DB
COPY init.sh .
