import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class GroupiewTests(BaseViewTests):

    @responses.activate
    def test_group_list_200_OK(self):
        add_response(
            'GET',
            'community/groups',
            body={'total': 1}
        )

        response = self.client.get(
            self.reverse('group-list'), {
                'q': 'group'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_create_200_OK(self):
        add_response(
            'POST',
            'community/createGroup',
            body={'success': True}
        )

        response = self.client.post(
            self.reverse('group-list'), {
                'title': 'my item',
                'access': 'public'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_detail_200_OK(self):
        add_response(
            'GET',
            'community/groups/test',
            body={'id': 'test'}
        )

        response = self.client.get(
            self.reverse('group-detail', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 'test')

    @responses.activate
    def test_group_update_200_OK(self):
        add_response(
            'POST',
            'community/groups/test/update',
            body={'title': 'updated'}
        )

        response = self.client.put(
            self.reverse('group-detail', args=('test',)), {
                'title': 'updated'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'updated')

    @responses.activate
    def test_group_delete_204_NO_CONTENT(self):
        add_response(
            'POST',
            'community/groups/test/delete',
            body={'success': True}
        )

        response = self.client.delete(
            self.reverse('group-detail', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
