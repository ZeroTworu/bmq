from asyncio import events

from app.config.types import APP_MODE
from app.manager import Manager


def run_app():
    loop = events.new_event_loop()
    events.set_event_loop(loop)

    manager = Manager(APP_MODE)

    loop.run_until_complete(manager.run())


if __name__ == '__main__':
    run_app()
