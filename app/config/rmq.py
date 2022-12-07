from os import getenv

RMQ_DSN = getenv('BMQ_RMQ_DSN', 'amqp://user:password@127.0.0.1/')

RMQ_ROUTING_KEY = getenv('BMQ_RMQ_ROUTING_KEY', 'bmq')

RMQ_QUEUE = getenv('BMQ_RMQ_QUEUE', 'bmq')
