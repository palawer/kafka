from kafka   import KafkaProducer
from config  import producer_config


def send_task(*args,topic='',**kwargs):
    """Entry point for each kafka-task creation
    
    Keyword arguments:
    topic  -- topic where current producer will send the task
    kwargs -- task parameters
    """
    producer = KafkaProducer(**producer_config)
    producer.send(topic, value=kwargs)
    producer.flush()
