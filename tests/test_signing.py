from django.test import TestCase

from certificates.generator import new_certificate
from certificates.models import Certificate


class MyTestCase(TestCase):
    fixtures = ['tests/fixtures.json']

    def test_sign_me(self):
        new_certificate(Certificate.objects.get(id=3), key_size=4096,
                        environment=2, deviceid='123', subject_dn='/C=PL/O=SMOK sp. z o. o./OU=RAPID Server/CN=123')
