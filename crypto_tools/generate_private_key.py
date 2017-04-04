"""Generate a private key."""

import argparse
import getpass
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


# Two good sources for this:
# First, the crpyto SE:
#   http://crypto.stackexchange.com/questions/1978/how-big-an-rsa-key-is-considered-secure-today
# this source helpfully includes a graph of known factorizations. There's a
# decent trendline on the graph. It's unfortunately outdated, but if the trend
# held then 1024 bit keys were factored in ~2016, which is in the past.
#
# 512-bit (**THE DEFAULT KEY SIZE IN OPENSSL**) has already been factored. This
# is this script's raison d'être.
#
# Another good source:
#   https://en.wikipedia.org/wiki/RSA_Factoring_Challenge#The_prizes_and_records
# This has some for-fun factor prizes; the highest prize claimed was for a 768
# bit key. The challenge has since been withdraw, so it is unknown if further
# prizes would have been claimed.
_MINIMUM_ALLOWED_KEY_SIZE = 2048


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Generate a new RSA private key. Output the resulting key in PEM'
            ' form to stdout.'
        )
    )
    parser.add_argument(
        '--key-length',
        action='store',
        default=2048,
        type=int,
        help='The length of the private key, in bits.',
    )
    parser.add_argument(
        '--do-not-encrypt',
        action='store_false',
        dest='encrypt',
        default='true',
        help=(
            'Don\'t encrpyt the resulting *PRIVATE* key material. The result'
            ' is sensitive: if you leak the private key, it\'s all over.'
        ),
    )

    pargs = parser.parse_args()

    if pargs.key_length < _MINIMUM_ALLOWED_KEY_SIZE:
        print(
            'The specified key length {} is too small, and considered'
            ' insecure by this script. Specify a key length of at least {}'
            ' bits.'.format(
                pargs.key_length, _MINIMUM_ALLOWED_KEY_SIZE,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    if pargs.encrypt:
        password = getpass.getpass()
    else:
        password = None

    generate_rsa_key(sys.stdout, pargs.key_length, password)


def generate_rsa_key(output_file, length_in_bits, password):
    """Generate a new RSA private key."""

    # We take the library's advice here: "If in doubt you should use 65537."
    # (https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
    public_exponent = 65537

    private_key = rsa.generate_private_key(
        public_exponent,
        length_in_bits,
        backend=default_backend(),
    )

    if password is None:
        encryption = serialization.NoEncryption()
    else:
        encryption = serialization.BestAvailableEncryption(
            password.encode('utf-8')
        )

    key_material = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        encryption,
    )

    output_file.write(key_material.decode('ascii'))


if __name__ == '__main__':
    main()
