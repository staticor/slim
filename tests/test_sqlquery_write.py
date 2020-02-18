import pytest
from peewee import SqliteDatabase, Model, IntegerField, TextField, BlobField
from slim.base.permission import A

from slim import Application, ALL_PERMISSION
from slim.base.sqlquery import SQLValuesToWrite
from slim.exception import InvalidPostData
from slim.support.peewee import PeeweeView
from tests.tools import make_mocked_view_instance

pytestmark = [pytest.mark.asyncio]
app = Application(cookies_secret=b'123456', permission=ALL_PERMISSION)
db = SqliteDatabase(":memory:")


class ATestModel(Model):
    num1 = IntegerField()
    str1 = TextField()

    class Meta:
        table_name = 'test'
        database = db


class ATestView(PeeweeView):
    model = ATestModel


async def test_value_write_normal():
    write = SQLValuesToWrite({
        'num1': 123,
        'str1': 'whatever'
    })
    view: PeeweeView = await make_mocked_view_instance(app, ATestView, 'POST', '/api/list/1')
    write.bind(view, None, None)


async def test_value_write_normal2():
    write = SQLValuesToWrite({
        'num1': 123,
        'str1': 456
    })
    view: PeeweeView = await make_mocked_view_instance(app, ATestView, 'POST', '/api/list/1')
    write.bind(view, None, None)
    assert write['str1'] == '456'


async def test_value_write_invalid():
    write = SQLValuesToWrite({
        'num1': 123,
        'str1': {}
    })
    view: PeeweeView = await make_mocked_view_instance(app, ATestView, 'POST', '/api/list/1')
    with pytest.raises(InvalidPostData) as e:
        write.bind(view, None, None)