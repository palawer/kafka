from json import dumps
from json import loads


db_config = {
    "database" : "postgres",
    "user"     : "postgres",
    "password" : "Pass2020!",
    "host"     : "127.0.0.1",
    "port"     : "5432",
}

#attribution: https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc
producer_config = {
    "value_serializer"  : lambda m: dumps(m).encode('utf-8'), 
    "bootstrap_servers" : ['localhost:9092'],
}
consumer_config = {
    "auto_offset_reset"  : 'earliest',
    "enable_auto_commit" : True,
    "group_id"           : 'my-group-1',
    "value_deserializer" : lambda m: loads(m.decode('utf-8')),
    "bootstrap_servers"  : ['localhost:9092']
}

collector_topic = "collector"
regexp_topic    = "regexp"