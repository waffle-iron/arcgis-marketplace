import responses

from django.test import TestCase
from arcgis_marketplace import factories

from .api.shortcuts import add_response


class ModelsTests(TestCase):

    def test_account_str(self):
        account = factories.AccountFactory()
        self.assertEqual(str(account), account.user.email)

    def test_account_dir(self):
        account = factories.AccountFactory()
        self.assertIn('access_token', dir(account))

    def test_account_getattribute(self):
        account = factories.AccountFactory()
        self.assertEqual(account.access_token, 'test')

    def test_account_social_auth(self):
        account = factories.AccountFactory()
        self.assertEqual(account.social_auth, account.user.social_auth.get())

    def test_account_client(self):
        account = factories.AccountFactory()
        self.assertEqual(account.client().access_token, account.access_token)

    def test_account_api(self):
        account = factories.AccountFactory()
        self.assertEqual(account.api.access_token, account.access_token)

    def test_account_api_default(self):
        account = factories.AccountFactory()
        account._api = True
        self.assertTrue(account.api)

    @responses.activate
    def test_account_refresh_expired_token(self):
        add_response(
            'GET',
            'oauth2/token/',
            body={
                'access_token': 'new!',
                'expires_in': 1800
            }
        )

        account = factories.ExpiredAccountFactory()
        account.refresh_expired_token()

        self.assertFalse(account.is_expired)
        self.assertEqual(account.access_token, 'new!')

    @responses.activate
    def test_me(self):
        add_response('GET', 'community/users/test', body={'test': True})

        account = factories.AccountFactory()
        account.me()

        self.assertTrue(account.test)

    def test_item_str(self):
        item = factories.ItemFactory()
        self.assertEqual(str(item), item.title)
