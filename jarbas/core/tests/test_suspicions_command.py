from unittest.mock import patch

from jarbas.core.management.commands.suspicions import Command
from jarbas.core.models import Reimbursement
from jarbas.core.tests import TestCase


class TestCommand(TestCase):

    def setUp(self):
        self.command = Command()
        self.file_name = 'suspicions.xz'


class TestSerializer(TestCommand):

    def test_serializer(self):
        expected = {
            'document_id': 42,
            'probability': 0.38,
            'suspicions': {
                'hypothesis_1': True,
                'hypothesis_3': True
            }
        }

        input = {
            'document_id': '42',
            'hypothesis_1': 'True',
            'hypothesis_2': 'False',
            'hypothesis_3': 'True',
            'probability': '0.38'
        }
        self.serializer(self.command, input, expected)


    def test_serializer_without_probability(self):
        expected = {
            'document_id': 42,
            'probability': None,
            'suspicions': {
                'hypothesis_1': True,
                'hypothesis_3': True
            }
        }

        input = {
            'document_id': '42',
            'hypothesis_1': 'True',
            'hypothesis_2': 'False',
            'hypothesis_3': 'True'
        }
        self.serializer(self.command, input, expected)

    def test_serializer_without_suspicions(self):
        expected = {
            'document_id': 42,
            'probability': None,
            'suspicions': None
        }

        input = {
            'document_id': '42',
            'hypothesis_1': 'False',
            'hypothesis_2': 'False',
            'hypothesis_3': 'False'
        }
        self.serializer(self.command, input, expected)


class TestCustomMethods(TestCommand):

    @patch('jarbas.core.management.commands.suspicions.Command.suspicions')
    @patch('jarbas.core.management.commands.suspicions.Command.schedule_update')
    @patch('jarbas.core.management.commands.suspicions.Command.update')
    def test_main(self, update, schedule_update, suspicions):
        self.main(self.command, update, schedule_update, suspicions)


    @patch.object(Reimbursement.objects, 'get')
    def test_schedule_update_existing_record(self, get):
        reimbursement = Reimbursement()
        get.return_value = reimbursement
        content = {
            'document_id': 42,
            'probability': 0.618,
            'suspicions': {'answer': 42}
        }
        self.command.queue = []
        self.command.schedule_update(content)
        get.assert_called_once_with(document_id=content['document_id'])
        self.assertEqual(content['probability'], reimbursement.probability)
        self.assertEqual(content['suspicions'], reimbursement.suspicions)
        self.assertEqual([reimbursement], self.command.queue)

    @patch.object(Reimbursement.objects, 'get')
    def test_schedule_update_non_existing_record(self, get):
        content = {'document_id': 42}
        self.schedule_update_non_existing_record(self.command, content, get)

    @patch('jarbas.core.management.commands.suspicions.bulk_update')
    @patch('jarbas.core.management.commands.suspicions.print')
    def test_update(self, print_, bulk_update):
        fields = ['probability', 'suspicions']
        self.update(self.command, fields, print_, bulk_update)

    def test_bool(self):
        self.assertTrue(self.command.bool('True'))
        self.assertTrue(self.command.bool('true'))
        self.assertTrue(self.command.bool('1'))
        self.assertTrue(self.command.bool('0.5'))
        self.assertFalse(self.command.bool('False'))
        self.assertFalse(self.command.bool('false'))
        self.assertFalse(self.command.bool('None'))
        self.assertFalse(self.command.bool('none'))
        self.assertFalse(self.command.bool('null'))
        self.assertFalse(self.command.bool('NULL'))
        self.assertFalse(self.command.bool('nil'))
        self.assertFalse(self.command.bool('0'))
        self.assertFalse(self.command.bool('0.0'))


class TestConventionMethods(TestCommand):

    @patch('jarbas.core.management.commands.suspicions.Command.suspicions')
    @patch('jarbas.core.management.commands.suspicions.Command.main')
    @patch('jarbas.core.management.commands.suspicions.os.path.exists')
    @patch('jarbas.core.management.commands.suspicions.print')
    def test_handler_with_options(self, print_, exists, main, suspicions):
        self.handler_with_options(self.command, print_, exists, main, suspicions)

    @patch('jarbas.core.management.commands.suspicions.Command.suspicions')
    @patch('jarbas.core.management.commands.suspicions.Command.main')
    @patch('jarbas.core.management.commands.suspicions.os.path.exists')
    @patch('jarbas.core.management.commands.suspicions.print')
    def test_handler_without_options(self, print_, exists, main, suspicions):
        self.handler_without_options(self.command, print_, exists, main, suspicions)

    @patch('jarbas.core.management.commands.suspicions.Command.suspicions')
    @patch('jarbas.core.management.commands.suspicions.Command.main')
    @patch('jarbas.core.management.commands.suspicions.os.path.exists')
    def test_handler_with_non_existing_file(self, exists, update, suspicions):
        self.handler_with_non_existing_file(self.command, exists, update, suspicions)


class TestFileLoader(TestCommand):

    @patch('jarbas.core.management.commands.suspicions.print')
    @patch('jarbas.core.management.commands.suspicions.lzma')
    @patch('jarbas.core.management.commands.suspicions.csv.DictReader')
    @patch('jarbas.core.management.commands.suspicions.Command.serialize')
    def test_suspicions(self, serialize, rows, lzma, print_):
        self.new_command(self.command, self.command.suspicions(),
                         serialize, rows, lzma, print_)


class TestAddArguments(TestCommand):

    def test_add_arguments(self):
        self.add_arguments(self.command)
