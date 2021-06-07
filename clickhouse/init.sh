#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE TABLE IF NOT EXISTS default.data
    (
        time DateTime64(3, 'UTC') CODEC(DoubleDelta),
        date Datetime('UTC') CODEC(DoubleDelta),
        symbol LowCardinality(String) CODEC(ZSTD(1)),
        open Float32 CODEC(ZSTD(1)),
        high Float32 CODEC(ZSTD(1)),
        low Float32 CODEC(ZSTD(1)),
        close Float32 CODEC(ZSTD(1)),
        volume_btc Float32 CODEC(ZSTD(1)),
        volume_usdt Float32 CODEC(ZSTD(1)),
        tradecount UInt32 CODEC(ZSTD(1))
    )
    ENGINE = MergeTree
    PARTITION BY toYYYYMM(time)
    ORDER BY (time);
EOSQL

cat *.csv | clickhouse-client --query="INSERT INTO data FORMAT CSV"
