FROM yandex/clickhouse-server

# Copy custom entrypoint
COPY ./custom-entrypoint.sh /custom-entrypoint.sh
RUN chmod 775 /custom-entrypoint.sh

# Install splunk forwarder
WORKDIR /opt
RUN wget -O splunkforwarder-8.2.2-87344edfcdb4-linux-2.6-amd64.deb 'https://d7wz6hmoaavd0.cloudfront.net/products/universalforwarder/releases/8.2.2/linux/splunkforwarder-8.2.2-87344edfcdb4-linux-2.6-amd64.deb'
RUN dpkg -i splunkforwarder*.deb
RUN rm splunkforwarder*.deb
COPY splunk/user-seed.conf ./splunkforwarder/etc/system/local/user-seed.conf

# Change owner of the splunk forwarder to clickhouse user
RUN chown -R clickhouse:clickhouse /opt/splunkforwarder

# Download some sample data
WORKDIR /docker-entrypoint-initdb.d
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_minute.csv
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_ETHUSDT_minute.csv
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_LTCUSDT_minute.csv
RUN wget --no-check-certificate https://www.cryptodatadownload.com/cdd/Binance_BNBUSDT_minute.csv

# Remove first two lines of every csv file
RUN sed -i '1,2d' *.csv

# Copy script to initialize DB
COPY init.sh .

# Run the container as clickhouse user
USER 101

ENTRYPOINT [ "/custom-entrypoint.sh" ]