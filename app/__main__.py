from asyncio import events

from app.config.types import APP_MODE
from app.manager import Manager
from app.rmq_wait import wait_for_rmq


def run_app():
    wait_for_rmq()  # For Docker use

    manager = Manager()
    loop = events.get_event_loop()
    loop.run_until_complete(manager.run(APP_MODE))


if __name__ == '__main__':
    run_app()
