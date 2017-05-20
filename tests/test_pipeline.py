from django.test import TestCase

from social_core.backends.arcgis import ArcGISOAuth2
from social_core.backends.oauth import OAuthAuth

from arcgis_marketplace import factories
from arcgis_marketplace.pipeline import update_or_create_account
from arcgis_marketplace.pipeline import update_token_expiration


class PipelineTests(TestCase):

    def test_update_or_create_account(self):
        backend = ArcGISOAuth2()
        user = factories.UserFactory()

        update_or_create_account(backend, user, dict(test=True))
        self.assertTrue(user.account.test)

    def test_update_or_create_account_unknown_backend(self):
        backend = OAuthAuth()
        user = factories.UserFactory()

        update_or_create_account(backend, user, dict())
        self.assertFalse(hasattr(user, 'account'))

    def test_update_token_expiration(self):
        account = factories.ExpiredAccountFactory()
        social_auth = account.social_auth
        social_auth.extra_data = dict(expires_in=1800)

        update_token_expiration(account, social_auth)
        self.assertFalse(account.is_expired)
