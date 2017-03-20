===============
``crypto-tool``
===============

``crypto-tool`` is a tool to make some common cryptographic operations less
painful. Currently, it just supports being fed in common cryptographic files
(X.509 certificates and RSA keys) and emits a textual version of them by
calling out to ``openssl``. (But saving the invoker the tedious need to type
the full ``openssl`` command.)

Example use::

    $ crypto_tool.py < my_cert.crt
    < text description of certificate >

    $ crypto_tool.py <  my_rsa_key.key
    < text description of RSA key >
