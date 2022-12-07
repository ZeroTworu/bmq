import socket
import time
from urllib.parse import urlparse

from app.config.rmq import RMQ_DSN


def wait_for_rmq():
    result = urlparse(RMQ_DSN)
    if result.port is None:
        port = 5672
    else:
        port = result.port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((result.hostname, port))
            s.close()
            time.sleep(5)
            break
        except socket.error:
            print('Wait rmq...')
            time.sleep(0.5)
