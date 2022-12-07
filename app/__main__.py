from app.manager import Manager
from app.config.types import APP_MODE
import asyncio


def run_app():
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete

    manager = Manager()
    run(manager.run(APP_MODE))


if __name__ == '__main__':
    run_app()
