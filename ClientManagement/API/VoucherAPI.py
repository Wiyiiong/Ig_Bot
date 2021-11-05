#  Copyright (c)  Ong Wi Yi .

from firebase_admin.exceptions import FirebaseError, NotFoundError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from ClientManagement.Class.Voucher.Voucher import Voucher
from ClientManagement.Exception.ExceptionHandler import RESOURCE_NOT_FOUND
from Config.FirebaseSetup import db

voucher_ref = db.collection('voucher')

voucher_bp = Blueprint('voucher', __name__)


@voucher_bp.route('/voucher/', methods=["POST"])
def create_voucher():
    """
    To create an entry of an voucher
    :return: JSON Response
    """
    try:
        voucher_type = request.form['voucher_type']
        value = request.form["value"]
        valid_duration = request.form['duration']
        name = request.form['name']

        voucher = Voucher(voucher_type, value, valid_duration, name)

        voucher_ref.add(voucher.to_dict())
        return jsonify({"success": True}), 201
    except FirebaseError as e:
        abort(e.code, description=e)
    except Exception as e:
        abort(500, description=e)


@voucher_bp.route('/voucher/', methods=["GET"])
def get_voucher():
    """
    Retrieve the voucher details or image in json format
    :return: json object of Voucher Response
    """
    try:
        tp = request.args.get("type")
        document_id = request.args.get("document")
        doc_ref = voucher_ref.document(str(document_id))
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if tp == "info":
                return jsonify({'success': True, 'data': data}), 200
            elif tp == "image":
                voucher = Voucher.from_dict(data)
                return jsonify({'success': True, 'data': voucher.generate_voucher_image()}), 200
        else:
            abort(404, description=RESOURCE_NOT_FOUND.format(document_id))
    except NotFoundError as e:
        abort(e.code, description=e)
    except FirebaseError as e:
        abort(e.code, description=e)
    except Exception as e:
        abort(500, description=e)