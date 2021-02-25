#!/usr/bin/env python

import argparse
import pyotp
import os

def get_secret_path(secret: str):
    current_path = os.path.dirname(os.path.abspath(__file__))
    if os.pathsep in secret:  #assume its path
        if os.path.isabs(secret) or not secret.startswith('.'):
            return secret
        else:
            return os.path.join(current_path, secret)
    else:  #assume it
        if not secret.endswith('.secret'):
            secret+='.secret'
        return os.path.join(current_path,'secrets', secret)


def get_totp(secret_path: str):
    with open(secret_path, 'r') as key:
        # for now secret is stored as a single line in file,
        # TODO: use .ini for example
        secret = key.readline().rstrip()
        totp = pyotp.totp.TOTP(secret)
        return totp.now()

def main(args):
    secret_path = get_secret_path(args.secret)
    #print(secret_path)
    print(get_totp(secret_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show (time based) OTP based on secret')
    parser.add_argument('secret', type=str)
    args = parser.parse_args()
    main(args)
