#!/usr/bin/env python3

import argparse
import io
import subprocess
import sys


def show_crypto_file(fileobj):
    data = fileobj.read(1 * 1024 * 1024)
    if len(data) == 1 * 1024 * 1024:
        print('Input is unconfortably large; aborting.', file=sys.stderr)
        sys.exit(1)

    io_obj = io.TextIOWrapper(io.BytesIO(data), 'ascii')
    first_line = next(iter(io_obj))
    if first_line == '-----BEGIN CERTIFICATE-----\n':
        # x509 certificate:
        openssl_call(('x509', '-text', '-noout'), data)
    elif first_line == '-----BEGIN RSA PRIVATE KEY-----\n':
        # RSA private key:
        openssl_call(('rsa', '-text', '-noout'), data)
    elif first_line == '-----BEGIN PRIVATE KEY-----\n':
        # OpenSSL RSA private key:
        openssl_call(('rsa', '-text', '-noout'), data)
    else:
        print('Not sure what kind of input that is.', file=sys.stderr)
        print(
            'Note that I\'ve not been trained to recognize CSRs yet,'
            ' though.',
            file=sys.stderr,
        )
        print(
            'Also note that I only recogize PEM (≈base64) encoded things.'
            ' I cannot recogize the DER (binary) variants yet.',
            file=sys.stderr,
        )
        sys.exit(1)


def openssl_call(args, stdin):
    proc = subprocess.Popen(
        ('openssl',) + args,
        stdin=subprocess.PIPE,
    )
    proc.communicate(stdin)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    pargs = parser.parse_args()

    if pargs.command is None:
        show_crypto_file(sys.stdin.buffer)


if __name__ == '__main__':
    main()
