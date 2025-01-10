
from flask import request, make_response, jsonify


def set_cookie(key, value):
    response = make_response(jsonify({"message":key, "value":value}))
    response.set_cookie(key, value, max_age=60*60*24*30)
    return response


def get_cookie(key):
    value = request.cookies.get(key)
    return value