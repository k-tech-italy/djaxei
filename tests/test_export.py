# see https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
import random

import pytest

from demoproject.app1.models import DemoModel4
from djaxei import Exporter


@pytest.mark.django_db
class TestEqual(object):

    def test_export(self, mocked_writer, records4):
        from demoproject.app1.models import DemoModel1, DemoModel2, DemoModel3
        root = random.choice(DemoModel1.objects.all())
        data = {
            'app1.demomodel1': ['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic', 'date', 'nullable', 'choice'],
            'app1.demomodel2': ['id', 'fk_id',  'integer'],
            'app1.DemoModel3': ['id', 'fk_id', 'char', 'integer'],
            'app1.DemoModel4': ['id',  'fk2_id', 'char', 'fk1_id', 'integer'],
        }
        workbook_filename = Exporter().xls_export(data, root=root)
        assert [r['data'] for r in mocked_writer['demomodel2']] == [data['app1.demomodel2'], ] + \
               [list(x) for x in root.demomodel2_set.values_list(*data['app1.demomodel2'])]
        assert [r['data'] for r in mocked_writer['demomodel3']] == [data['app1.DemoModel3'], ] + \
               [list(x) for x in root.demomodel3_set.values_list(*data['app1.DemoModel3'])]
        assert [r['data'] for r in mocked_writer['demomodel4']] == [data['app1.DemoModel4'], ] + \
               [list(x) for x in DemoModel4.objects.filter(fk1__fk=root).values_list(*data['app1.DemoModel4'])]
