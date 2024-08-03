# events/backends.py
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import Group

class CustomOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)
        self._assign_user_groups(user, claims)
        return user

    def update_user(self, user, claims):
        user = super().update_user(user, claims)
        self._assign_user_groups(user, claims)
        return user

    def _assign_user_groups(self, user, claims):
        if 'realm_access' in claims:
            roles = claims['realm_access'].get('roles', [])
            for role in roles:
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)
