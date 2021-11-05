#  Copyright (c)  Ong Wi Yi .
from flask import Blueprint, jsonify

errors_bp = Blueprint('errors', __name__)

RESOURCE_NOT_FOUND = "Resource requested {} not found."


@errors_bp.app_errorhandler(400)
def handle_bad_request_error(error):
    response = {'code': 400, 'type': "Bad Request", 'error': {'message': str(error.description)}}
    return jsonify(response), 400


@errors_bp.app_errorhandler(401)
def handle_unauthorized_error(error):
    response = {'code': 401, 'type': "Unauthorized", 'error': {'message': str(error.description)}}
    return jsonify(response), 401


@errors_bp.app_errorhandler(403)
def handle_forbidden_error(error):
    response = {'code': 403, 'type': "Forbidden", 'error': {'message': str(error.description)}}
    return jsonify(response), 403


@errors_bp.app_errorhandler(404)
def handle_not_found_error(error):
    response = {'code': 404, 'type': "Resource Not Found Exception", 'error': {'message': str(error.description)}}
    return jsonify(response), 404


@errors_bp.app_errorhandler(405)
def handle_method_not_allowed_error(error):
    response = {'code': 405, 'type': "Method Not Allowed", 'error': {'message': str(error.description)}}
    return jsonify(response), 405


@errors_bp.app_errorhandler(500)
def handle_unexpected_error(error):
    response = {'code': 500, 'type': "Internal Server Error", 'error': {'message': str(error.description)}}
    return jsonify(response), 500


@errors_bp.app_errorhandler(503)
def handle_service_error(error):
    response = {'code': 503, 'type': "Service Unavailable", 'error': {'message': str(error.description)}}
    return jsonify(response), 503