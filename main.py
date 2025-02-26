import io

import clickhouse_connect
import fastavro
from confluent_kafka import Consumer, KafkaException

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "pg_server.public.my_table"
SCHEMA_REGISTRY_URL = "http://schema-registry:8081"

# ClickHouse connection
# client = clickhouse_connect.get_client(host="clickhouse", port=8123)

# Kafka consumer config
conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "clickhouse_consumer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}

consumer = Consumer(conf)
consumer.subscribe([KAFKA_TOPIC])


def decode_avro_message(msg_value):
    """Avro ma'lumotlarini json formatiga o'girish"""
    bytes_io = io.BytesIO(msg_value)
    reader = fastavro.reader(bytes_io)
    return [record for record in reader][0]


print("Listening for messages...")

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaException._PARTITION_EOF:
            continue
        else:
            print(f"Consumer error: {msg.error()}")
            break

    try:
        data = decode_avro_message(msg.value())
        print(f"Received message: {data}")

        # client.insert(
        #     "my_table",
        #     [[data["id"], data["name"], data["amount"]]],
        #     column_names=["id", "name", "amount"],
        # )
        consumer.commit()

    except Exception as e:
        print(f"Error processing message: {e}")

consumer.close()
