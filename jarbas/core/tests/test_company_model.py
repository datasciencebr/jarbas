from django.test import TestCase
from jarbas.core.models import Company
from jarbas.core.tests import sample_activity_data, sample_company_data


class TestCreate(TestCase):

    def setUp(self):
        self.data = sample_company_data

    def test_create(self):
        self.assertEqual(0, Company.objects.count())
        company = Company.objects.create(**self.data)
        company.save()
        self.assertEqual(1, Company.objects.count())
        self.assertEqual(1, len(company.main_activity))
        self.assertEqual(1, len(company.secondary_activity))
