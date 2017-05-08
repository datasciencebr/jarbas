from datetime import date
from io import StringIO
from unittest.mock import MagicMock, call, patch

from django.test import TestCase

from jarbas.core.management.commands.companies import Command
from jarbas.core.models import Company


class TestCommand(TestCase):

    def setUp(self):
        self.command = Command()


class TestSerializer(TestCommand):

    def test_to_email(self):
        expected = 'jane@example.com'
        self.assertEqual(self.command.to_email('abc'), None)
        self.assertEqual(self.command.to_email('jane@example.com'), expected)

    def test_serializer(self):
        company = {
            'email': 'ahoy',
            'opening': '31/12/1969',
            'situation_date': '31/12/1969',
            'special_situation_date': '31/12/1969',
            'latitude': '3.1415',
            'longitude': '-42',
            'main_activity': 'Main Act.',
            'main_activity_code': '1001'
        }
        for i in range(1, 100):
            company['secondary_activity_{}'.format(i)] = 'Act. {}'.format(i)
            company['secondary_activity_{}_code'.format(i)] = str(i)

        expected = {
            'email': None,
            'opening': date(1969, 12, 31),
            'situation_date': date(1969, 12, 31),
            'special_situation_date': date(1969, 12, 31),
            'latitude': 3.1415,
            'longitude': -42.0,
            'main_activity': [{'code': '1001', 'description': 'Main Act.'}]
        }
        expected['secondary_activity'] = [
            {'code': str(i), 'description': 'Act. {}'.format(i)}
            for i in range(1, 100)
        ]

        self.assertEqual(self.command.serialize(company), expected)


class TestCreate(TestCommand):

    @patch('jarbas.core.management.commands.companies.Command.print_count')
    @patch('jarbas.core.management.commands.companies.Command.bulk_create')
    def test_bulk_create_by(self, bulk_create, print_count):
        self.command.count = 0
        self.command.bulk_create_by(range(0, 10), 4)
        bulk_create.assert_has_calls((
            call([0, 1, 2, 3]),
            call([4, 5, 6, 7]),
            call([8, 9])
        ))

    @patch.object(Company.objects, 'bulk_create')
    @patch('jarbas.core.management.commands.companies.Command.print_count')
    def test_bulk_create(self, print_count, bulk_create):
        self.command.count = 0
        self.command.bulk_create(list(range(0, 3)))
        bulk_create.assert_called_once_with([0, 1, 2])
        print_count.assert_called_once_with(Company, count=3)
        self.assertEqual(3, self.command.count)


class TestConventionMethods(TestCommand):

    @patch('jarbas.core.management.commands.companies.print')
    @patch('jarbas.core.management.commands.companies.LoadCommand.drop_all')
    @patch('jarbas.core.management.commands.companies.Command.bulk_create_by')
    @patch('jarbas.core.management.commands.companies.Command.print_count')
    def test_handler_without_options(self, print_count, bulk_create_by, drop_all, print_):
        print_count.return_value = 0
        self.command.handle(dataset='companies.xz', batch_size=42)
        print_.assert_called_with('Starting with 0 companies')
        self.assertEqual(1, bulk_create_by.call_count)
        self.assertEqual(1, print_count.call_count)
        self.assertEqual('companies.xz', self.command.path)
        drop_all.assert_not_called()

    @patch('jarbas.core.management.commands.companies.print')
    @patch('jarbas.core.management.commands.companies.Command.drop_all')
    @patch('jarbas.core.management.commands.companies.Command.bulk_create_by')
    @patch('jarbas.core.management.commands.companies.Command.print_count')
    def test_handler_with_options(self, print_count, bulk_create_by, drop_all, print_):
        print_count.return_value = 0
        self.command.handle(dataset='companies.xz', batch_size=42, drop=True)
        print_.assert_called_with('Starting with 0 companies')
        self.assertEqual(1, drop_all.call_count)
        self.assertEqual(1, bulk_create_by.call_count)

    def test_add_arguments(self):
        parser = MagicMock()
        self.command.add_arguments(parser)
        self.assertEqual(3, parser.add_argument.call_count)


class TestCustomMethods(TestCommand):

    def test_is_valid(self):
        expects_true = (
            'main_activity_code',
            'cnpj',
            'trade_name',
            'secondary_activity_42',
            'secondary_activity_42_code'
        )
        expects_false = (
            'secondary_activity',
            'secondary_activity_100',
            'secondary_activity_100_code',
            'ahoy'
        )
        for value in expects_true:
            with self.subTest():
                self.assertTrue(self.command.is_valid(value), value)
        for value in expects_false:
            with self.subTest():
                self.assertFalse(self.command.is_valid(value), value)


class TestFileLoader(TestCommand):

    @patch('jarbas.core.management.commands.companies.lzma')
    @patch('jarbas.core.management.commands.companies.csv.DictReader')
    @patch('jarbas.core.management.commands.companies.Company')
    @patch('jarbas.core.management.commands.companies.Command.serialize')
    def test_reimbursement_property(self, serializer, company, row, lzma):
        lzma.return_value = StringIO()
        row.return_value = [dict(main_activity='ahoy')]
        self.command.path = 'companies.xz'
        list(self.command.companies)
        self.assertEqual(1, company.call_count)
