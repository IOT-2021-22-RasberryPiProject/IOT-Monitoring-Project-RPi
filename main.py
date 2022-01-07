#!/usr/bin/env python3
from sender import Sender
from config import CONFIG


def main():
    sender = Sender(CONFIG)
    sender.start()


if __name__ == '__main__':
    main()
