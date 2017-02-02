import pandas
import lzma

from jarbas.core.management.commands import LoadCommand
from jarbas.core.models import Reimbursement


class Command(LoadCommand):
    help = 'Load Serenata de Amor reimbursements dataset'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--batch-size', '-b', dest='batch_size', type=int, default=10000,
            help='Number of documents to be created at a time (default: 10000)'
        )

        parser.add_argument(
                '--irregularities-path', '-i', dest='irregularities_path',
                help='Path to irregularities dataset')

    def handle(self, *args, **options):
        self.reimbursements_path = options['dataset']
        self.irregularities_path = options['irregularities_path']
        self.count = Reimbursement.objects.count()
        print('Starting with {:,} reimbursements'.format(self.count))

        if options.get('drop', False):
            self.drop_all(Reimbursement)
            self.count = 0

        self.bulk_create_by(self.reimbursements, options['batch_size'])
        self.print_count(Reimbursement, count=self.count, permanent=True)

    @property
    def reimbursements(self):
        """Returns a Generator with a Reimbursement object for each row."""
        with lzma.open(self.reimbursements_path, mode='rt') as reimbursements_file,lzma.open(
                        self.irregularities_path, mode='rt') as irregularities_file:
            
            file_handler = pandas.merge(pandas.read_csv(reimbursements_file, dtype=object).fillna(''), 
                                        pandas.read_csv(irregularities_file, dtype=object).fillna(''), 
                                        on=['applicant_id','year','document_id'])
            
            for index, row in file_handler.iterrows():
                print(row.to_dict())
                #yield Reimbursement(**self.serialize(row.to_dict()))

    def serialize(self, reimbursement):
        """Read the dict generated by DictReader and fix content types"""

        missing = ('probability', 'suspicions')
        for key in missing:
            reimbursement[key] = None

        rename = (
            ('subquota_number', 'subquota_id'),
            ('reimbursement_value_total', 'total_reimbursement_value')
        )
        for old, new in rename:
            reimbursement[new] = reimbursement[old]
            del reimbursement[old]

        integers = (
            'applicant_id',
            'batch_number',
            'congressperson_document',
            'congressperson_id',
            'document_id',
            'document_type',
            'installment',
            'month',
            'subquota_group_id',
            'subquota_id',
            'term',
            'term_id',
            'year'
        )
        for key in integers:
            reimbursement[key] = self.to_number(reimbursement[key], int)

        floats = (
            'document_value',
            'remark_value',
            'total_net_value',
            'total_reimbursement_value'
        )
        for key in floats:
            reimbursement[key] = self.to_number(reimbursement[key])

        reimbursement['issue_date'] = self.to_date(reimbursement['issue_date'])

        return reimbursement

    def bulk_create_by(self, reimbursements, size):
        batch = list()
        for reimbursement in reimbursements:
            batch.append(reimbursement)
            if len(batch) == size:
                self.bulk_create(batch)
                batch = list()
        self.bulk_create(batch)

    def bulk_create(self, batch):
        Reimbursement.objects.bulk_create(batch)
        self.count += len(batch)
        self.print_count(Reimbursement, count=self.count)
