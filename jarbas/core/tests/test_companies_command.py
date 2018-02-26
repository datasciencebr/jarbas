import datetime
import os
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from jarbas.core.management.commands.companies import Command
from jarbas.core.models import Activity, Company


class TestCommand(TestCase):

    def setUp(self):
        self.command = Command()


class TestCreate(TestCommand):

    @patch.object(Activity.objects, 'update_or_create')
    def test_save_activities(self, update_or_create):
        company = {
            'main_activity_code': '42',
            'main_activity': 'Ahoy'
        }
        for num in range(1, 100):
            company['secondary_activity_{}_code'.format(num)] = 100 + num
            company['secondary_activity_{}'.format(num)] = str(num)

        main, secondaries = self.command.save_activities(company)
        self.assertEqual(100, update_or_create.call_count)
        self.assertIsInstance(main, list)
        self.assertIsInstance(secondaries, list)
        self.assertEqual(1, len(main))
        self.assertEqual(99, len(secondaries))

    @patch('jarbas.core.management.commands.companies.Command.save_activities')
    @patch('jarbas.core.management.commands.companies.Command.print_count')
    @patch.object(Company.objects, 'create')
    def test_save_companies(self, create, print_count, save_activities):
        self.command.count = 0
        save_activities.return_value = ([3], [14, 15])
        self.command.path = os.path.join(settings.BASE_DIR, 'jarbas', 'core', 'tests',
                                         'fixtures', 'companies.xz')
        self.command.save_companies()
        expected = {
                    'additional_address_details': b'', 'address': b'',
                    'city': b'', 'cnpj': b'', 'email': 'test@test.com.br', 'last_updated': b'',
                    'latitude': -15.7910966, 'legal_entity': b'', 'longitude': -47.9508743,
                    'name': 'Test', 'neighborhood': b'', 'number': 1, 'opening': None,
                    'phone': b'', 'responsible_federative_entity': b'',
                    'situation': b'', 'zip_code': b'', 'situation_date': datetime.date(2005, 9, 24),
                    'situation_reason': b'', 'type': 'Book', 'special_situation_date': None,
                    'state': b'', 'status': b'', 'trade_name': b'', 'special_situation': b''
                    }
        create.assert_called_with(**expected)
        create.return_value.main_activity.add.assert_called_with(3)
        self.assertEqual(1, print_count.call_count)
        self.assertEqual(2, create.return_value.secondary_activity.add.call_count)


class TestConventionMethods(TestCommand):

    @patch('jarbas.core.management.commands.companies.print')
    @patch('jarbas.core.management.commands.companies.LoadCommand.drop_all')
    @patch('jarbas.core.management.commands.companies.Command.save_companies')
    @patch('jarbas.core.management.commands.companies.Command.print_count')
    def test_handler_without_options(self, print_count, save_companies, drop_all, print_):
        print_count.return_value = 0
        self.command.handle(dataset='companies.xz')
        print_.assert_called_with('Starting with 0 companies')
        self.assertEqual(1, save_companies.call_count)
        self.assertEqual(1, print_count.call_count)
        self.assertEqual('companies.xz', self.command.path)
        drop_all.assert_not_called()

    @patch('jarbas.core.management.commands.companies.print')
    @patch('jarbas.core.management.commands.companies.Command.drop_all')
    @patch('jarbas.core.management.commands.companies.Command.save_companies')
    @patch('jarbas.core.management.commands.companies.Command.print_count')
    def test_handler_with_options(self, print_count, save_companies, drop_all, print_):
        print_count.return_value = 0
        self.command.handle(dataset='companies.xz', drop=True)
        print_.assert_called_with('Starting with 0 companies')
        self.assertEqual(2, drop_all.call_count)
        self.assertEqual(1, save_companies.call_count)
