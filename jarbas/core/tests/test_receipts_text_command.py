from unittest.mock import patch

from jarbas.core.management.commands.receipts_text import Command
from jarbas.core.models import Reimbursement
from jarbas.core.tests import TestCase


class TestCommand(TestCase):

    def setUp(self):
        self.command = Command()
        self.file_name = 'receipts-texts.xz'


class TestSerializer(TestCommand):

    def test_serializer(self):
        expected = {
            'document_id': 42,
            'receipt_text': 'lorem ipsum',
        }

        input = {
            'document_id': '42',
            'text': 'lorem ipsum'
        }
        self.serializer(self.command, input, expected)

    def test_serializer_without_text(self):
        expected = {
            'document_id': 42,
            'receipt_text': None
        }

        input = {
            'document_id': '42',
        }
        self.serializer(self.command, input, expected)


class TestCustomMethods(TestCommand):

    @patch('jarbas.core.management.commands.receipts_text.Command.receipts')
    @patch('jarbas.core.management.commands.receipts_text.Command.schedule_update')
    @patch('jarbas.core.management.commands.receipts_text.Command.update')
    def test_main(self, update, schedule_update, receipts):
        self.main(self.command, update, schedule_update, receipts)

    @patch.object(Reimbursement.objects, 'get')
    def test_schedule_update_existing_record(self, get):
        reimbursement = Reimbursement()
        get.return_value = reimbursement
        content = {
            'document_id': 42,
            'receipt_text': 'lorem ipsum'
        }
        self.command.queue = []
        self.command.schedule_update(content)
        get.assert_called_once_with(document_id=42)
        self.assertEqual(content['receipt_text'], reimbursement.receipt_text)
        self.assertEqual([reimbursement], self.command.queue)

    @patch.object(Reimbursement.objects, 'get')
    def test_schedule_update_non_existing_record(self, get):
        content = {'document_id': 42}
        self.schedule_update_non_existing_record(self.command, content, get)

    @patch('jarbas.core.management.commands.receipts_text.bulk_update')
    @patch('jarbas.core.management.commands.receipts_text.print')
    def test_update(self, print_, bulk_update):
        fields = ['receipt_text',]
        self.update(self.command, fields, print_, bulk_update)


class TestConventionMethods(TestCommand):

    @patch('jarbas.core.management.commands.receipts_text.Command.receipts')
    @patch('jarbas.core.management.commands.receipts_text.Command.main')
    @patch('jarbas.core.management.commands.receipts_text.os.path.exists')
    @patch('jarbas.core.management.commands.receipts_text.print')
    def test_handler_with_options(self, print_, exists, main, receipts):
        self.handler_with_options(self.command, print_, exists, main, receipts)

    @patch('jarbas.core.management.commands.receipts_text.Command.receipts')
    @patch('jarbas.core.management.commands.receipts_text.Command.main')
    @patch('jarbas.core.management.commands.receipts_text.os.path.exists')
    @patch('jarbas.core.management.commands.receipts_text.print')
    def test_handler_without_options(self, print_, exists, main, receipts):
        self.handler_without_options(self.command, print_, exists, main, receipts)

    @patch('jarbas.core.management.commands.receipts_text.Command.receipts')
    @patch('jarbas.core.management.commands.receipts_text.Command.main')
    @patch('jarbas.core.management.commands.receipts_text.os.path.exists')
    def test_handler_with_non_existing_file(self, exists, update, receipts):
        self.handler_with_non_existing_file(self.command, exists, update, receipts)


class TestFileLoader(TestCommand):

    @patch('jarbas.core.management.commands.receipts_text.print')
    @patch('jarbas.core.management.commands.receipts_text.lzma')
    @patch('jarbas.core.management.commands.receipts_text.csv.DictReader')
    @patch('jarbas.core.management.commands.receipts_text.Command.serialize')
    def test_receipts(self, serialize, rows, lzma, print_):
        self.new_command(self.command, self.command.receipts(),
                         serialize, rows, lzma, print_)


class TestAddArguments(TestCommand):

    def test_add_arguments(self):
        self.add_arguments(self.command)
