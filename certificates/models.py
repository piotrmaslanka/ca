from django.db import models


class Certificate(models.Model):
    public_key = models.TextField()
    private_key = models.TextField()
    is_used_for_client_auth = models.BooleanField(default=False, verbose_name='Can this certificate be used for signing '
                                                                              'certificates that are meant to be used '
                                                                              'as client authentication?')
    is_ca = models.BooleanField(default=False,
                                verbose_name='Can this certificate be used for signing certificates that sign other'
                                             'certificates?')
    can_sign = models.BooleanField(default=False,
                                   verbose_name='Can this certificate be used for signing other certificates?')
    common_name = models.CharField(max_length=255)
    # if following is null, that means it's self-signed
    signed_by = models.ForeignKey('certificates.Certificate', on_delete=models.RESTRICT, null=True, blank=True)
    serial = models.CharField(max_length=16)

    class Meta:
        unique_together = ('serial', 'signed_by')

    def __str__(self) -> str:
        return self.common_name

