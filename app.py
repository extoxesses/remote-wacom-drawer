import asyncio
import sys
from app import logger, sio, SERVER

async def main() -> None:
    try:
        logger.info(f'Connecting to server at {SERVER}')
        # worker.start()
        await sio.connect(SERVER)
        while True:
            try:
                #await sio.sleep(1)
                await sio.wait()
            except KeyboardInterrupt:
                logger.info("Received Ctrl+C, shutting down...")
                await sio.disconnect()
                sys.exit(0)
    except Exception as e:
        logger.error(f"Connection error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())