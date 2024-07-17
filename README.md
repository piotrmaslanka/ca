ca
==

The certificate authority Web interface.

Basically a Web interface to openssl genrsa, req and ca.

You:

1. Like to store private keys alongside public keys.
2. Use LDAP to authenticate.

This software enables you to:

* issue new certificates with custom fields (as in custom OID).

It also stores all of the private keys, and supports only "I'll generate you a private key" mode.
