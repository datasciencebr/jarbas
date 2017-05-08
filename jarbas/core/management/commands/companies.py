import csv
import lzma
from functools import partial
from re import compile

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from jarbas.core.management.commands import LoadCommand
from jarbas.core.models import Company


class Command(LoadCommand):
    help = 'Load Serenata de Amor companies dataset into the database'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--batch-size', '-b', dest='batch_size',
            type=int, default=10000,
            help='Number of companies to be created at a time'
        )

    def handle(self, *args, **options):
        self.path = options['dataset']
        self.count = self.print_count(Company)
        print('Starting with {:,} companies'.format(self.count))

        if options.get('drop', False):
            self.drop_all(Company)
            self.count = 0

        self.bulk_create_by(self.companies, options['batch_size'])

    @property
    def companies(self):
        """
        Receives path to the dataset file and create a Company object for
        each row of each file. It creates the related activity when needed.
        """
        with lzma.open(self.path, mode='rt') as file_handler:
            for row in csv.DictReader(file_handler):
                keys = list(filter(self.is_valid, row.keys()))
                filtered = {k: v for k, v in row.items() if k in keys}
                obj = Company(**self.serialize(filtered))

                yield obj

    @staticmethod
    def serialize_activity(row, key):
        if isinstance(key, int):
            key = 'secondary_activity_{}'.format(key)

        activity = dict(
            code=row.get('{}_code'.format(key)),
            description=row.get(key)
        )

        if any(activity.values()):
            return activity

    def serialize_activities(self, row):
        activity_from = partial(self.serialize_activity, row)
        main = [activity_from('main_activity')]
        secondary = [activity_from(i) for i in range(1, 100)]

        row['main_activity'] = [a for a in main if a is not None]
        row['secondary_activity'] = [a for a in secondary if a is not None]

        rx = compile(r'^(main|secondary)(_activity_)(([\d]+)|(code))(_code)?$')
        cleanup = [k for k in row.keys() if rx.match(k)]
        for key in cleanup:
            del row[key]

        return row

    def serialize(self, row):
        row['email'] = self.to_email(row['email'])

        dates = ('opening', 'situation_date', 'special_situation_date')
        for key in dates:
            row[key] = self.to_date(row[key])

        decimals = ('latitude', 'longitude')
        for key in decimals:
            row[key] = self.to_number(row[key])

        return self.serialize_activities(row)

    @staticmethod
    def to_email(email):
        try:
            validate_email(email)
            return email

        except ValidationError:
            return None

    def bulk_create_by(self, companies, size):
        batch = list()
        for company in companies:
            batch.append(company)
            if len(batch) == size:
                self.bulk_create(batch)
                batch = list()
        self.bulk_create(batch)
        self.print_count(Company, count=self.count, permanent=True)

    def bulk_create(self, batch):
        Company.objects.bulk_create(batch)
        self.count += len(batch)
        self.print_count(Company, count=self.count)

    def is_valid(self, field):
        if field == 'secondary_activity':
            return False

        if field == 'main_activity_code':
            return True

        if field in (f.name for f in Company._meta.fields):
            return True

        regex = compile(r'^secondary_activity_([\d]{1,2})(_code)?$')
        return bool(regex.match(field))
