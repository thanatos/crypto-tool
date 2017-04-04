================
``crypto-tools``
================

``crypto-tools`` is a python library containing tools to make some common
cryptographic operations less painful. Currently, it supports:

* ``generate_private_key``: Generating private RSA keys.
* ``show_file``: Displaying a textual version of some common cryptographic
  files.


``generate_private_key``
========================

Generates an RSA private key. Mostly, this is to encode sane defaults into a
script, since ``openssl``'s defaults are insecure.


``show_file``
=============

Currently, it just supports being fed in common cryptographic files
(X.509 certificates and RSA keys) and emits a textual version of them by
calling out to ``openssl``. (But saving the invoker the tedious need to type
the full ``openssl`` command.)

Example use::

    $ python -m crypto_tools.show_file < my_cert.crt
    < text description of certificate >

    $ python -m crypto_tools.show_file < my_rsa_key.key
    < text description of RSA key >
