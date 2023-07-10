import os
import logging


def get_input_url():
    return os.getenv('INPUT_URL')


def get_output_file():
    return os.getenv('OUTPUT_FILE')


def get_proxy():
    proxy_ = os.getenv('PROXY')

    auth, server = proxy_.split('@')
    usr, pswrd = auth.split(':')
    if ' ' in server:
        server = server.replace(' ', '')

    proxy = {
        'server': server,
        'username': usr,
        'password': pswrd
    }

    return proxy


def configure_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
