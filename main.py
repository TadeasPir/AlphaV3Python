import logging

from config.config import Config
from src.server import TCPServer
def main():

    # Load configuration
    try:
        config = Config("../AlphaV3Python/config/config.yaml")
    except Exception as e:
        logging.error(f"Error during execution: {e}")

    server = TCPServer(config)


    try:
        server.run()
        logging.info(f"Server started successfully")

    except Exception as e:
        logging.error(f"Error during execution: {e}")
        server.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logging.info(f"interuped by keyboard: {e}")


