import json
import os
import subprocess
import sys
from datetime import datetime
from django.contrib.auth.models import User
from satella.files import read_re_sub_and_write, read_in_file

from certificates.models import Certificate
from signing.models import Signing, SignatureDatabase
from .conf_gen import save_to_disk, get_current_serial


def new_certificate(signed_by: Certificate, issuer: User, key_size: int = 4096, days=365, country: str = 'PL',
                    organisation: str = 'SMOK sp. z o. o.', org_unit='Production', common_name: str = 'CN',
                    **kwargs) -> Certificate:
    """
    Create a new certificate

    :param signed_by: certificate that this one will be signed by
    :param key_size: key size (RSA)
    :param days: validity period
    :param country:
    :param organisation:
    :param org_unit:
    :param common_name:
    :param kwargs:
    :return:
    """
    assert sys.platform == 'linux', 'This can run only on Linux'
    sign = Signing.objects.get(certificate=signed_by)
    save_to_disk(sign, **kwargs)
    base_path = os.path.join('/ssl', str(sign.id))
    for key, value in kwargs.items():
        read_re_sub_and_write(os.path.join(base_path, 'openssl.conf'), key.upper(), str(value))

    subject_dn = f'/C={country}/O={organisation}/OU={org_unit}/CN={common_name}'

    rc = subprocess.Popen(['openssl', 'genrsa', '-out', f'/ssl/{sign.id}/cert.key', str(key_size)],
                          stdout=sys.stdout, stderr=sys.stdout)
    rc.wait()
    if rc.returncode:
        raise RuntimeError('failed')
    rc = subprocess.Popen(
        ['openssl', 'req', '-new', '-key', f"/ssl/{sign.id}/cert.key", '-out', f'/ssl/{sign.id}/cert.csr', '-config',
         f'/ssl/{sign.id}/openssl.conf',
         '-subj', subject_dn],
        stdout=sys.stdout, stderr=sys.stdout)
    rc.wait()
    if rc.returncode:
        raise RuntimeError('failed')

    rc = subprocess.Popen(
        ['openssl', 'ca', '-batch', '-extensions', 'dev_cert', '-config', f'/ssl/{sign.id}/openssl.conf', '-in',
         f'/ssl/{sign.id}/cert.csr'],
        stdout=sys.stdout, stderr=sys.stdout)
    rc.wait()
    if rc.returncode:
        raise RuntimeError('failed')

    # Find our new cert
    cert_name = os.listdir(os.path.join(base_path, 'newcerts'))[0]
    cert_path = os.path.join(base_path, 'newcerts', cert_name)

    end_date = subprocess.Popen(['openssl', 'x509', '-enddate', '-noout', '-in', cert_path],
                                stdout=subprocess.PIPE)
    end_date.wait()
    read_data = end_date.stdout.read().decode('utf-8')
    read_data = read_data.replace('notAfter=', '').replace('\n', '')
    expiration = datetime.strptime(read_data, '%b %d %H:%M:%S %Y %Z').strftime("%y%m%d%H%M%SZ")

    cert = Certificate(public_key=read_in_file(cert_path, encoding='utf-8'),
                       private_key=read_in_file(os.path.join(base_path, 'cert.key'), encoding='utf-8'),
                       signed_by=signed_by, serial=sign.next_serial.rjust(16, '0'), common_name=subject_dn,
                       extra_data=json.dumps(kwargs))
    cert.save()
    prev_serial = sign.next_serial
    sign.next_serial = get_current_serial(sign)
    sign.save()

    db_entry = SignatureDatabase(signing=sign, status='V', expiration=expiration, serial=prev_serial,
                                 subject_dn=subject_dn, certificate=cert, signed_by=signed_by)
    db_entry.save()

    return cert
