import sys
from app import logger, sio, SERVER

def main() -> None:
    try:
        logger.info(f'Connecting to server at {SERVER}')
        sio.connect(SERVER)
        while True:
            try:
                sio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received Ctrl+C, shutting down...")
                sio.disconnect()
                sys.exit(0)
    except Exception as e:
        logger.error(f"Connection error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()