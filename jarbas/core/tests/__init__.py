from io import StringIO
from datetime import date
from random import randrange

from unittest.mock import Mock, call

from django.utils import timezone
from django.test import TestCase as DjangoTestCase

from jarbas.core.models import Reimbursement, Tweet


class TestCase(DjangoTestCase):

    def serializer(self, command, input, expected):
        serialized = command.serialize(input)
        self.assertEqual(serialized, expected)

    def main(self, command, update, schedule_update, custom_method):
        custom_method.return_value = (range(21), range(21, 43))
        command.main()
        update.assert_has_calls([call()] * 2)
        schedule_update.assert_has_calls(call(i) for i in range(42))

    def schedule_update_non_existing_record(self, command, content, get):
        get.side_effect = Reimbursement.DoesNotExist
        command.queue = []
        command.schedule_update(content)
        get.assert_called_once_with(document_id=42)
        self.assertEqual([], command.queue)

    def update(self, command, fields, print_, bulk_update):
        command.count = 40
        command.queue = list(range(2))
        command.update()
        bulk_update.assert_called_with([0, 1], update_fields=fields)
        print_.assert_called_with('42 reimbursements updated.', end='\r')
        self.assertEqual(42, command.count)

    def handler_with_options(self, command, print_, exits, main, custom_command):
        command.handle(dataset=self.file_name, batch_size=42)
        main.assert_called_once_with()
        print_.assert_called_once_with('0 reimbursements updated.')
        self.assertEqual(command.path, self.file_name)
        self.assertEqual(command.batch_size, 42)

    def handler_without_options(self, command, print_, exits, main, custom_command):
        command.handle(dataset=self.file_name, batch_size=4096)
        main.assert_called_once_with()
        print_.assert_called_once_with('0 reimbursements updated.')
        self.assertEqual(command.path, self.file_name)
        self.assertEqual(command.batch_size, 4096)

    def handler_with_non_existing_file(self, command, exists, update, custom_command):
        exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            command.handle(dataset='suspicions.xz', batch_size=4096)
        update.assert_not_called()

    def new_command(self, command, custom_command, serialize, rows, lzma, print_):
        serialize.return_value = '.'
        lzma.return_value = StringIO()
        rows.return_value = range(42)
        command.batch_size = 10
        command.path = self.file_name
        expected = [['.'] * 10, ['.'] * 10, ['.'] * 10, ['.'] * 10, ['.'] * 2]
        self.assertEqual(expected, list(custom_command))
        self.assertEqual(42, serialize.call_count)

    def add_arguments(self, command):
        mock = Mock()
        command.add_arguments(mock)
        self.assertEqual(2, mock.add_argument.call_count)


suspicions = {
    'over_monthly_subquota': {'is_suspect': True, 'probability': 1.0}
}

sample_reimbursement_data = dict(
    applicant_id=13,
    batch_number=9,
    cnpj_cpf='11111111111111',
    congressperson_document=2,
    congressperson_id=1,
    congressperson_name='Roger That',
    document_id=42,
    document_number='6',
    document_type=7,
    document_value=8.90,
    installment=7,
    issue_date=date(1970, 1, 1),
    leg_of_the_trip='8',
    month=1,
    net_values='1.99,2.99',
    party='Partido',
    passenger='John Doe',
    reimbursement_numbers='10,11',
    reimbursement_values='12.13,14.15',
    remark_value=1.23,
    state='UF',
    subquota_description='Subquota description',
    subquota_group_description='Subquota group desc',
    subquota_group_id=5,
    subquota_id=4,
    supplier='Acme',
    term=1970,
    term_id=3,
    total_net_value=4.56,
    total_reimbursement_value=None,
    year=1970,
    probability=0.5,
    suspicions=suspicions
)

sample_activity_data = dict(
    code='42',
    description='So long, so long, and thanks for all the fish'
)

sample_company_data = dict(
    cnpj='12.345.678/9012-34',
    opening=date(1995, 9, 27),
    legal_entity='42 - The answer to life, the universe, and everything',
    trade_name="Don't panic",
    name='Do not panic, sir',
    type='BOOK',
    status='OK',
    situation='EXISTS',
    situation_reason='Douglas Adams wrote it',
    situation_date=date(2016, 9, 25),
    special_situation='WE LOVE IT',
    special_situation_date=date(1997, 9, 28),
    responsible_federative_entity='Vogons',
    address='Earth',
    number='',
    additional_address_details='',
    neighborhood='',
    zip_code='',
    city='',
    state='',
    email='',
    phone='',
    last_updated=timezone.now(),
    latitude=None,
    longitude=None
)


def random_tweet_status():
    """
    Fixture generators (mixer, and faker behind the scenes) won't generate a
    value for a `DecimalField` with zero decimal places — which is the case of
    Tweet.status (too big to fit `BigIntegerField`). Therefore we use this
    function to workaround random test fixtures for Tweet.status.
    """
    status = Tweet._meta.get_field('status')
    min_range = 9223372036854775807  # max big integer should be the minimum
    max_range = 10 ** status.max_digits  # field limit
    return randrange(min_range, max_range)
