#!/usr/bin/python3
"""
New view for State objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/api/v1/states', strict_slashes=False)
def all_states():
    """ retrieve list of all State objects """
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def retrieve_state(state_id):
    """ retrieve a particular State """
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
        return state
    except:
        abort(404)


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a State """
    state = storage.get('State', state_id)
    if state:
        state.delete()
        storage.save()
        return {}
    abort(404)


@app_views.route('/api/v1/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ create a State """
    state_name = request.get_json()
    if not state_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in state_name:
        abort(400, {'Missing name'})
    new_state = State(**state_name)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ update a State """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_state = storage.get('State', state_id)
    if not my_state:
        abort(404)
    for key, value in update_attr.items():
        setattr(my_state, key, value)
    storage.save()
    return my_state.to_dict()
