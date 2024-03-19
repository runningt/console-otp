#!/usr/bin/env python

import argparse
import pyotp
import os

SECRETS_STORE = 'secrets'
SECRET_EXT = '.secret'

def get_secret_path(secret: str):
    current_path = os.path.dirname(os.path.abspath(__file__))
    if os.pathsep in secret:  #assume its path
        if os.path.isabs(secret) or not secret.startswith('.'):
            return secret
        else:
            return os.path.join(current_path, secret)
    else:  #assume it
        if not secret.endswith(SECRET_EXT):
            secret+=SECRET_EXT
        return os.path.join(current_path, SECRETS_STORE, secret)


def get_secret_list(path=SECRETS_STORE):
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_path, SECRETS_STORE)
    return [os.path.splitext(f)[0] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(SECRET_EXT)]

def list_secrets(secrets: list):
    print("Secrets:")
    for secret in secrets:
        print(f"{secret}")

def get_totp(secret: str):
    secret_path = get_secret_path(secret)
    with open(secret_path, 'r') as key:
        # for now secret is stored as a single line in file,
        # TODO: use .ini for example
        secret = key.readline().rstrip()
        totp = pyotp.totp.TOTP(secret)
        return totp.now()

def get_file(secret: str):
    secret_path = get_secret_path(secret)
    with open(secret_path, 'r') as f:
        return f"{secret}: {f.read()}"

def main(args):
    if args.list:
        list_secrets(get_secret_list())
    elif args.secret:
        print(get_totp(args.secret))
    elif args.print:
        print(get_file(args.print))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show (time based) OTP based on secret')
    parser.add_argument('secret', nargs="?", type=str)
    parser.add_argument('-l', '--list', help="List stored secrets", action='store_true')
    parser.add_argument('-p', '--print', type=str, help="Print secret")
    args = parser.parse_args()
    main(args)
