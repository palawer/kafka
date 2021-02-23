from tasks.regexp.consumer import start
import os
import logging
basename,ext = os.path.splitext(
    os.path.basename(__file__)
)
logging.basicConfig(
    format='%(asctime)s: %(pathname)s:%(lineno)d  [%(levelname)s] -> %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/collector.log"),
    ]
)
logging.getLogger('kafka').setLevel(logging.ERROR) #hide kafka traces
if __name__== "__main__":
    start()