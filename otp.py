#!/usr/bin/env python

import argparse
import pyotp
import os


def main(args):
    secret_name = args.secret
    with open(args.secret, 'r') as key:
        # for now secret is stored as a single line in file,
        # TODO: use .ini for example
        secret = key.readline().rstrip()
        totp = pyotp.totp.TOTP(secret)
        print(totp.now())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show (time based) OTP based on secret')
    parser.add_argument('secret', type=str)
    args = parser.parse_args()
    main(args)
