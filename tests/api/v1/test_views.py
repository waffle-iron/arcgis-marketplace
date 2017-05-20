import arcgis_sdk
import json
import responses

from django.urls import reverse
from rest_framework import status
from core_flavor.api.test import APITestCase

from arcgis_marketplace import factories


class ViewsTests(APITestCase):

    # Accounts
    @responses.activate
    def test_account_list_200_OK(self):
        account = factories.AccountFactory(user__is_staff=True)
        import ipdb; ipdb.set_trace()
        self.client.force_authenticate(user=account.user)

        responses.add(
            responses.GET,
            arcgis_sdk.ARCGIS_API_URL + 'community/users/test',
            body=json.dumps({
                'test': True
            }),
            status=200,
            content_type='application/json'
        )

        response = self.client.get(
            reverse('arcgis-marketplace-api:v1:account-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], account.id.hex)

    def _test_account_list_403_FORBIDDEN(self):
        self.client._credentials['HTTP_ACCEPT'] = 'application/json'

        account = factories.AccountFactory()
        self.client.force_authenticate(user=account.user)

        response = self.client.get(
            reverse('arcgis-marketplace-api:v1:account-list')
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
