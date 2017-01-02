import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from passlib.apps import custom_app_context as pwd_context


class NewRoot(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'add'),
        # (Allow, Authenticated, 'secret'),
    ]


def check_credentials(username, password):
    """Return True if correct username and password, else False."""
    stored_username = os.environ["AUTH_USERNAME"]
    store_password = os.environ["AUTH_PASSWORD"]
    if username and password:
        if username == stored_username:
            return pwd_context.verify(password, store_password)
    return False


def includeme(config):
    """Security-related configuration."""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(NewRoot)
