import datetime
import logging
from datetime import datetime


def main():
    logging.basicConfig(filename=f'../logs/uav-logs-{str(datetime.utcnow()).replace(":", "-")}.log', level=logging.CRITICAL)
    object_name = ''
    while object_name != 'q':
        object_name = str(input())
        now = datetime.utcnow()
        logging.critical(f'Object {object_name} logged at {now}')


if __name__ == '__main__':
    main()
