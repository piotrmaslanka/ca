import os

from satella.coding import silence_excs
from satella.files import write_to_file, read_in_file

from signing.models import Signing


class ListAppender:
    def __init__(self, lst: list[str], tag: str):
        self.lst = lst
        try:
            self.index = lst.index(tag)
        except ValueError:
            self.lst.append(tag)
            self.index = lst.index(tag)

    def add(self, s: str) -> None:
        self.lst.insert(self.index + 1, s)


def sane_split(split: str) -> list[str]:
    if '\r\n' in split:
        return split.split('\r\n')
    else:
        return split.split('\n')


def find_in_ssl(ssl: list[str], opt: str) -> int:
    try:
        return ssl.index(opt)
    except ValueError:  # is not in list
        ssl.append(opt)
        return ssl.index(opt)


def mkdir_for(signing: Signing) -> None:
    """Make a directory for a particular signing"""
    base_path = os.path.join('/ssl', str(signing.id))


def save_database_to_disk(signing: Signing) -> None:
    base_path = os.path.join('/ssl', str(signing.id))
    with open(os.path.join(base_path, 'index.txt'), 'w', encoding='utf-8') as fout:
        for db_entry in signing.signaturedatabase_set.all():
            fout.write(
                f'{db_entry.status}\t{db_entry.expiration}\t{db_entry.revocation}\t{db_entry.serial.rjust(16, "0")}\t'
                f'unknown\t{db_entry.subject_dn}\n')


@silence_excs(FileExistsError)
def try_mkdir(dir: str) -> None:
    os.mkdir(dir)


def sanitize_kwargs(kwargs: dict) -> dict:
    new_dict = {}
    for key, value in kwargs.items():
        new_dict[key.lower()] = value
    return new_dict


def save_to_disk(signing: Signing, **kwargs) -> None:
    base_path = os.path.join('/ssl', str(signing.id))
    try_mkdir(base_path)
    try_mkdir(os.path.join(base_path, 'certs'))
    try_mkdir(os.path.join(base_path, 'crl_dir'))
    try_mkdir(os.path.join(base_path, 'newcerts'))
    try_mkdir(os.path.join(base_path, 'keys'))
    try_mkdir(os.path.join(base_path, 'csrs'))

    write_to_file(os.path.join(base_path, 'signing.pem'),
                  signing.certificate.public_key, encoding='utf-8')
    write_to_file(os.path.join(base_path, 'signing.key'),
                  signing.certificate.private_key, encoding='utf-8')
    save_database_to_disk(signing)
    write_to_file(os.path.join(base_path, 'serial'), signing.next_serial.rjust(16, '0'), encoding='utf-8')

    data = generate_openssl_configuration(signing, **kwargs)
    write_to_file(os.path.join(base_path, 'openssl.conf'), data.strip(), encoding='utf-8')


def get_current_serial(signing: Signing) -> str:
    return read_in_file(os.path.join('/ssl', str(signing.id), 'serial'), encoding='utf-8').rjust(16, '0')


def add_ca_root_smok(openssl: list[str], signing: Signing):
    la = ListAppender(openssl, '[ CA_ROOT_SMOK ]')
    base_path = os.path.join('/ssl', str(signing.id))
    la.add('certs=$dir/certs')
    la.add('crl_dir=$dir/crl_dir')
    la.add('database=$dir/index.txt')
    la.add('new_certs_dir=$dir/newcerts')
    la.add('serial=$dir/serial')
    la.add('certificate=$dir/signing.pem')
    la.add('private_key=$dir/signing.key')
    la.add('crl=$dir/crl.pem')
    la.add(f'dir=/ssl/{signing.id}')


def generate_openssl_configuration(signing: Signing, **kwargs) -> str:
    kwargs = sanitize_kwargs(kwargs)
    openssl = sane_split(signing.openssl_conf)

    if '[ v3_ca ]' in openssl:
        return generate_ca_configuration(signing)

    # Input extra fields
    la = ListAppender(openssl, '[ req_cert ]')
    for field in signing.signingfield_set.all():
        field_name = field.name.lower()
        la.add(f'{field.oid}={field.type}:{kwargs[field_name]}')

    la = ListAppender(openssl, '[ dev_oids ]')
    for field in signing.signingfield_set.all():
        la.add(f'{field.name}={field.oid}')

    la = ListAppender(openssl, '[ dev_cert ]')
    for field in signing.signingfield_set.all():
        field_name = field.name.lower()
        la.add(f'{field.oid}={field.type}:{kwargs[field_name]}')

    if signing.certificate.is_ca:
        la.add('basicConstraints=critical,CA:TRUE')
    else:
        la.add('basicConstraints=critical,CA:FALSE')

    if signing.certificate.is_used_for_client_auth:
        la.add('extendedKeyUsage = critical,clientAuth,serverAuth')
    else:
        la.add('extendedKeyUsage = critical,serverAuth')

    la = ListAppender(openssl, '[ req_distinguished_name ]')
    for field in signing.signingfield_set.all():
        la.add(f'{field.name}={field.name}')

    add_ca_root_smok(openssl, signing)

    openssl_config = '\n'.join([*openssl, ''])
    return openssl_config
