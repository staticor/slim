import time

import pytest

from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from peewee import *
from slim import Application, ALL_PERMISSION
from slim.utils import get_ioloop
from slim.tools.test import make_mocked_view_instance, invoke_interface

pytestmark = [pytest.mark.asyncio]
app = Application(cookies_secret=b'123456', permission=ALL_PERMISSION)
db = SqliteDatabase(":memory:")


class Topic(Model):
    title = CharField(index=True, max_length=255)
    time = BigIntegerField(index=True)
    content = TextField()

    class Meta:
        database = db


db.create_tables([Topic], safe=True)


Topic.create(time=time.time(), title='Hello', content='World')
Topic.create(time=time.time(), title='Hello2', content='World')
Topic.create(time=time.time(), title='Hello3', content='World')
Topic.create(time=time.time(), title='Hello4', content='World')


@app.route.view('topic')
class TopicView(PeeweeView):
    model = Topic


app._prepare()


async def test_view_get():
    resp = await invoke_interface(app, TopicView().get, params={'title': 'Hello'})
    assert resp.ret_val['data']['title'] == 'Hello'


async def test_view_get_failed():
    resp = await invoke_interface(app, TopicView().get, params={'title': 'Hello_not_here'})
    assert resp.ret_val['code'] == RETCODE.NOT_FOUND
