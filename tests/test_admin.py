from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from arcgis_marketplace import admin
from arcgis_marketplace import models


class MockRequest:
    pass


request = MockRequest()


class AdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_admin_account(self):
        model_admin = admin.AccountAdmin(models.Account, self.site)
        self.assertIn('user', model_admin.get_fields(request))

    def test_admin_webmapingapp(self):
        model_admin = admin.WebMapingAppAdmin(models.WebMapingApp, self.site)
        self.assertIn('title', model_admin.get_fields(request))
