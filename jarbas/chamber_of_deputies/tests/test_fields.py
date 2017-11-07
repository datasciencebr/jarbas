from django.test import TestCase

from jarbas.chamber_of_deputies.fields import DateAsStringField


class TestDateAsStringField(TestCase):

    def test_deserialize(self):
        dates = (
            '2017-12-31 00:00:00',
            '2017-12-31T00:00:00',
            '2017-12-31'
        )
        expected = '2017-12-31'
        for dt in dates:
            with self.subTest():
                self.assertEqual(expected, DateAsStringField.deserialize(dt))
