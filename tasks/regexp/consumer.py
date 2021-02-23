from kafka import KafkaConsumer
from json import loads
from config import regexp_topic
from config import consumer_config
from tasks.regexp.process import run
from tasks.send_task import send_task


def start(*args,**kwargs):
    consumer = KafkaConsumer(
        regexp_topic,
        **consumer_config
    )
    for m in consumer:
        snapshot_id = run(**m.value)
