import json
import uuid
import ldap3
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings


class LDAPAuthentication(BaseBackend):
    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    def get_user_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous or not user_obj.is_active:
            return set()
        result = set()
        for p_type, p_model in itertools.product(['change', 'view', 'add', 'delete'],
                                                 ['contenttype', 'session', 'certificate']):
            result.add(f'{p_type}_{p_model}')
        return result

    def get_all_permissions(self, user_obj, obj=None):
        return self.get_user_permissions(user_obj, obj=obj)

    def has_perm(self, user_obj, perm, obj=None):
        if 'group' in perm:
            return False
        if user_obj.is_anonymous or not user_obj.is_active:
            return False
        return True

    def authenticate(self, request, username=None, password=None, **kwargs):
        ldap_conn = ldap3.Server(settings.LDAP_HOST, get_info=ldap3.ALL)
        ldap_username = settings.LDAP_USER_BUILD.format(username=username)
        conn = ldap3.Connection(ldap_conn, user=ldap_username,
                                password=password, authentication=ldap3.SIMPLE, pool_keepalive=10)
        if not conn.bind():
            return None
        conn.unbind()

        ldap_conn = ldap3.Server(settings.LDAP_HOST, get_info=ldap3.ALL)
        conn = ldap3.Connection(ldap_conn, user=settings.LDAP_USERNAME, password=settings.LDAP_PASSWORD,
                                pool_keepalive = 10, authentication=ldap3.SIMPLE)
        if not conn.bind():
            raise RuntimeError('Could not connect to LDAP')
        conn.search(search_base=settings.LDAP_GROUP, search_filter='(objectClass=groupOfNames)',
                    attributes=ldap3.ALL_ATTRIBUTES)
        entries = json.loads(conn.response_to_json())
        members = entries['entries'][0]['attributes']['member']

        if ldap_username not in members:
            return None

        # Obtain info about the user
        conn.search(search_base=ldap_username, search_filter='(objectClass=inetOrgPerson)',
                    attributes=ldap3.ALL_ATTRIBUTES)
        entries = json.loads(conn.response_to_json())

        def getThing(thing: str) -> str:
            return entries['entries'][0]['attributes'][thing][0]

        givenName = getThing('givenName')
        email = getThing('mail')
        lastName = getThing('sn')

        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            u = User(username=username, first_name=givenName, last_name=lastName, email=email,
                     password=uuid.uuid4().hex, is_staff=True, is_active=True, is_superuser=True)
            u.save()

        u.is_staff = True
        u.is_superuser = True

        return u

    def get_user(self, user_id):
        return User.objects.get(id=user_id)
