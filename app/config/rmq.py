from os import getenv

RMQ_DSN = getenv('BMQ_RMQ_DSN', 'amqp://user:password@127.0.0.1/')
