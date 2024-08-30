import json
from flask import Flask, request, jsonify
import logging
import sys

from ModelDAO.Persist.MongoDBPerist import MongoDBPersist
from ModelDAO.Event.EventDAO import EventDAO
from ModelDAO.Event.Event import Event
from Utils.Tokens import Tokens


app = Flask(__name__)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


valid_tokens = Tokens()

def valid_token_only_read(token):
    is_valid = valid_tokens.token_is_exist(token)
    if is_valid: logger.info('Token válido para leitura')
    else: logger.info('Token inválido para leitura')
    return is_valid


def valid_token_admin(token):
    is_valid = valid_tokens.token_is_admin(token)
    if is_valid: logger.info('Token de admin, válido para leitura e escrita')
    else: logger.info('Token não é de admin, válido para leitura mas inválido para escrita')
    return is_valid


@app.route('/get_events', methods=['GET'])
def get_events():
    logger.info('Início chamada get_events')
    token = request.headers.get('Authorization')
    is_valid = valid_token_only_read(token)
    if not is_valid: 
        logger.info('Fim chamada get_events')
        return {'token': 'token inválido'}

    top = request.args.get('top')

    logger.info('Início consulta eventos no banco')
    events = EventDAO(
        MongoDBPersist(
            name_database='test_mongo',
            client='mongodb://localhost:27017/',
            collection='events'
        )
    ).getAllEvents(top=int(top))

    logger.info('Fim consulta eventos no banco')
    dc_events = [
        {
            'event_name': ev['event_name'], 
            'address': ev['address'], 
            'start_date': ev['start_date'], 
            'end_date': ev['end_date']
        } for ev in events
    ]
    logger.info('Fim chamada get_events')
    return {'events': dc_events}


@app.route('/get_event_by_name', methods=['GET'])
def get_event_by_name():
    logger.info('Início chamada get_event_by_name')
    token = request.headers.get('Authorization')
    is_valid = valid_token_only_read(token)
    if not is_valid: 
        logger.info('Fim chamada get_event_by_name')
        return {'token': 'token inválido'}

    name = request.args.get('name')
    logger.info('Início consulta eventos no banco')
    events = EventDAO(
        MongoDBPersist(
            name_database='test_mongo',
            client='mongodb://localhost:27017/',
            collection='events'
        )
    ).getEventByName(name)

    logger.info('Fim consulta eventos no banco')
    dc_events = [
        {
            'event_name': ev['event_name'], 
            'address': ev['address'], 
            'start_date': ev['start_date'], 
            'end_date': ev['end_date']
        } for ev in events
    ]
    logger.info('Fim chamada get_event_by_name')
    return {'events': dc_events}


@app.route('/insert_event', methods=['POST'])
def insert_event():
    logger.info('Início chamada insert_event')
    token = request.headers.get('Authorization')
    is_valid = valid_token_admin(token)
    if not is_valid: 
        logger.info('Fim chamada insert_event')
        return {'token': 'token inválido'}

    event_name = request.args.get('name')
    address = request.args.get('address')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    logger.info('Início insert de evento no banco')
    EventDAO(
        MongoDBPersist(
            name_database='test_mongo',
            client='mongodb://localhost:27017/',
            collection='events'
        )
    ).insertEvents(events=Event(event_name=event_name, address=address, start_date=start_date, end_date=end_date))

    logger.info('Fim insert de evento no banco')
    logger.info('Fim chamada insert_event')
    return {'result': "insert realizado com sucesso"}


@app.route('/update_address', methods=['POST'])
def update_address():
    logger.info('Início chamada update_address')
    token = request.headers.get('Authorization')
    is_valid = valid_token_admin(token)
    if not is_valid: 
        logger.info('Fim chamada update_address')
        return {'token': 'token inválido'}

    event_name = request.args.get('name')
    address = request.args.get('address')

    logger.info('Início update evento no banco')
    EventDAO(
        MongoDBPersist(
            name_database='test_mongo',
            client='mongodb://localhost:27017/',
            collection='events'
        )
    ).updateAddress(event_name, new_values={"address": address})

    logger.info('Fim update evento no banco')
    logger.info('Fim chamada update_address')
    return {'result': "update realizado com sucesso"}


@app.route('/delete_event', methods=['POST'])
def delete_event():
    logger.info('Início chamada delete_event')
    token = request.headers.get('Authorization')
    is_valid = valid_token_admin(token)
    if not is_valid: 
        logger.info('Fim chamada delete_event')
        return {'token': 'token inválido'}

    event_name = request.args.get('name')

    logger.info('Início delete evento no banco')
    EventDAO(
        MongoDBPersist(
            name_database='test_mongo',
            client='mongodb://localhost:27017/',
            collection='events'
        )
    ).deleteEvent(event_name=event_name)


    logger.info('Fim delete evento no banco')
    logger.info('Fim chamada delete_event')
    return {'result': "delete realizado com sucesso"}

# app.run(host='0.0.0.0', port=80)
app.run()
