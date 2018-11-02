from dateutil import parser
from pingout.__init__ import create_app

def test_return_200_on_root(client):
    """ Return status code 200 on root url"""
    response = client.get('/')
    assert response.status_code == 200

def test_create_pingout(client):
    response = client.post('create-pingout')
    response2 = client.get('create-pingout')
    assert response.status_code == 201
    assert response2.status_code == 405

def test_bad_format_pingout(client):
    uuid = '12345678aq234123ac12423a'
    response = client.get(f'/{uuid}')
    assert response.status_code == 400

def test_invalid_pingout(client):
    uuid = '9e46643f534c4807adb2d7691188242a'
    response = client.get(f'/{uuid}')
    assert response.status_code == 404

def test_valid_pingout(client):
    pingout = client.post('/create-pingout')
    uuid = pingout.json['uuid']
    client.post(f'/{uuid}/ping')
    pingout = client.get(f'/{uuid}')
    assert pingout.status_code == 200

def test_pingout_invalid_date_rage(client):
    pingout = client.post('/create-pingout')
    uuid = pingout.json['uuid']
    initial_date = parser.parse('2018-11-02')
    final_date = parser.parse('2018-11-01')
    pingout = client.get(f'/{uuid}/filter/?initial_date={initial_date}&final_date={final_date}')
    assert pingout.status_code == 404
