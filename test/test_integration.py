# test_integration.py
from typing import Dict, Any

import pytest
from mock import patch

from json import loads

from app import create_app


clients : Dict[str, Any] = {}
def new_post(url, **argsw):
    url = url[len('http://'):]
    bar_pos = url.find('/')

    node = url[:bar_pos]
    service = url[bar_pos+1:]

    clients[node].post(service, **argsw)

@patch('app.requests.post', side_effect=new_post)
def test_client_receive(mocked_post):
    client1 = create_app(my_ip='a').test_client()
    clients['a'] =client1

    client2 = create_app(my_ip='b', servers=['a']).test_client()
    clients['b'] = client2

    res = client2.get('blockchain')
    assert res.status_code == 200

    res = loads(client1.get('getips').get_data(as_text=True))
    assert res == ['b']
