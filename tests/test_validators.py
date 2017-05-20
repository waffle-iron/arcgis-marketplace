from django.core import exceptions
from django.test import TestCase

from arcgis_marketplace import factories
from arcgis_marketplace.validators import validate_file_extension
from arcgis_marketplace.validators import validate_zip_compression


class ValidatorsTests(TestCase):

    def test_validate_file_extension(self):
        obj = factories.WebMapingAppFactory()
        validate_file_extension(obj.file)

    def test_validate_file_extension_validation_error(self):
        obj = factories.WebMapingAppFactory(file__filename='test.txt')

        with self.assertRaises(exceptions.ValidationError):
            validate_file_extension(obj.file)

    def test_validate_zip_compression(self):
        obj = factories.WebMapingAppFactory(file__from_path='tests/test.zip')

        validate_zip_compression(obj.file)

    def test_validate_zip_compression_validation_error(self):
        obj = factories.WebMapingAppFactory()

        with self.assertRaises(exceptions.ValidationError):
            validate_zip_compression(obj.file)
