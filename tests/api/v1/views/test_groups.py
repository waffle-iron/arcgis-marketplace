import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class GroupiewTests(BaseViewTests):

    @responses.activate
    def test_group_create_200_OK(self):
        add_response(
            'POST',
            'content/users/test/addItem',
            body={'success': True}
        )

        response = self.client.post(
            self.reverse('group-list'), {
                'title': 'my item',
                'type': 'Web Mapping Application'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    @responses.activate
    def test_group_detail_200_OK(self):
        add_response(
            'GET',
            'content/items/itemId',
            body={'id': 'test'}
        )

        response = self.client.get(
            self.reverse('group-detail', args=('itemId',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 'test')

    @responses.activate
    def test_group_share_200_OK(self):
        add_response(
            'POST',
            'content/items/itemId/share',
            body={'itemId': 'test'}
        )

        response = self.client.post(
            self.reverse('group-share', args=('itemId',)), {
                'groups': 'group1,group2'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
