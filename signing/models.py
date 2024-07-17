from django.db import models


class Signing(models.Model):
    """This represents a way to sign a certificate"""
    certificate = models.ForeignKey('certificates.Certificate', on_delete=models.RESTRICT,
                                    help_text='Certificate that will serve as a signer',
                                    unique=True)
    openssl_conf = models.TextField(verbose_name='OpenSSL configuration file',
                                    help_text='Take a look at sample attached openssl.conf')
    name = models.CharField(max_length=200)
    next_serial = models.CharField(max_length=16, verbose_name='Next serial to use for signing')

    def __str__(self) -> str:
        return self.name


class SigningField(models.Model):
    signing = models.ForeignKey(Signing, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    oid = models.CharField(max_length=255, verbose_name='According to RFC3061')
    type = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.signing.name} - {self.name}'


STATUS = [
    ('V', 'valid'),
    ('R', 'revoked'),
    ('E', 'expired')
]

class SignatureDatabase(models.Model):
    signing = models.ForeignKey(Signing, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=1)
    expiration = models.CharField(max_length=20)
    revocation = models.CharField(max_length=20, default='', blank=True)
    serial = models.CharField(max_length=16)
    subject_dn = models.CharField(max_length=255)
    certificate = models.ForeignKey('certificates.Certificate', on_delete=models.CASCADE,
                                    verbose_name='Certificate that was issued as a result of this',
                                    related_name='certificates')
    signed_by = models.ForeignKey('certificates.Certificate', on_delete=models.CASCADE,
                                  verbose_name='Certificate that has signed this one', null=True,
                                  related_name='signers')

    def __str__(self):
        return f'{self.subject_dn}'
