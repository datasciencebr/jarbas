from datetime import date
from unittest.mock import Mock, patch

from jarbas.core.management.commands import LoadCommand
from jarbas.core.models import Activity
from jarbas.core.tests import TestCase, sample_activity_data


class TestCommand(TestCase):

    def setUp(self):
        self.command = LoadCommand()

class TestStaticMethods(TestCommand):

    def test_get_model_name(self):
        self.assertEqual('Activity', self.command.get_model_name(Activity))

    def test_to_date(self):
        expected = date(1991, 7, 22)
        self.assertEqual(self.command.to_date('22/7/91'), expected)
        self.assertEqual(self.command.to_date('1991-07-22 03:15:00+0300'), expected)
        self.assertEqual(self.command.to_date('22/13/91'), None)
        self.assertEqual(self.command.to_date('aa/7/91'), None)
        self.assertEqual(self.command.to_date('22/07/16'), date(2016, 7, 22))

    def test_to_number(self):
        self.assertIsNone(self.command.to_number(''))
        self.assertIsNone(self.command.to_number('NaN'))
        self.assertIsNone(self.command.to_number('nan'))
        self.assertEqual(1.0, self.command.to_number('1'))
        self.assertEqual(1.2, self.command.to_number('1.2'))
        self.assertEqual(1, self.command.to_number('1', int))
        self.assertEqual(1, self.command.to_number('1.0', int))


class TestPrintCount(TestCommand):

    @patch('jarbas.core.management.commands.print')
    def test_print_no_records(self, mock_print):
        self.command.print_count(Activity)
        arg = 'Current count: 0 Activitys                                    '
        kwargs = {'end': '\r'}
        mock_print.assert_called_with(arg, **kwargs)

    @patch('jarbas.core.management.commands.print')
    def test_print_with_records(self, mock_print):
        Activity.objects.create(**sample_activity_data)
        self.command.print_count(Activity)
        arg = 'Current count: 1 Activitys                                    '
        kwargs = {'end': '\r'}
        mock_print.assert_called_with(arg, **kwargs)

    @patch('jarbas.core.management.commands.print')
    def test_print_with_permanent_keyword_arg(self, mock_print):
        self.command.print_count(Activity, permanent=True)
        arg = 'Current count: 0 Activitys                                    '
        kwargs = {'end': '\n'}
        mock_print.assert_called_with(arg, **kwargs)


class TestDropAll(TestCommand):

    @patch('jarbas.core.management.commands.print')
    def test_drop_all(self, mock_print):
        self.assertEqual(0, Activity.objects.count())
        Activity.objects.create(**sample_activity_data)
        self.assertEqual(1, Activity.objects.count())
        LoadCommand().drop_all(Activity)
        self.assertEqual(0, Activity.objects.count())


class TestAddArguments(TestCommand):

    def test_add_arguments(self):
        self.add_arguments(self.command)

    def test_add_arguments_without_drop_all(self):
        mock = Mock()
        LoadCommand().add_arguments(mock, add_drop_all=False)
        self.assertEqual(1, mock.add_argument.call_count)
