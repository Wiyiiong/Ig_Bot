#  Copyright (c)  Ong Wi Yi .
from datetime import datetime

from firebase_admin.exceptions import FirebaseError, NotFoundError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from ClientManagement.Class.Voucher.Voucher import date_format, Voucher
from ClientManagement.Exception.ExceptionHandler import RESOURCE_NOT_FOUND
from ClientManagement.Util.VoucherCodeGenerator import VoucherCodeGenerator
from Config.FirebaseSetup import setup_firebase

db = setup_firebase()
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

        docs = voucher_ref.stream()
        code_lists = [d.id for d in docs]
        code = VoucherCodeGenerator.generate_code(code_lists)

        voucher = Voucher(voucher_type, value, int(valid_duration), name, code)

        voucher_ref.document(voucher.code).set(voucher.to_dict())
        return jsonify({"success": True}), 201
    except FirebaseError as e:
        abort(e.code, description=e)
    except Exception as e:
        abort(500, description=e)


@voucher_bp.route('/vouchers/', methods=["GET"])
def get_vouchers():
    """
    Retrieve all voucher from the database
    :return: List of vouchers
    """
    try:
        docs = voucher_ref.stream()
        data = [d.to_dict() for d in docs]
        return jsonify({'success': True, 'data': data}), 200

    except FirebaseError as e:
        abort(e.code, description=e)
    except TypeError as e:
        abort(500, description=e)


@voucher_bp.route('/voucher/<id>', methods=["GET"])
def get_voucher(id):
    """
    Retrieve the voucher details or image in json format
    :return: json object of Voucher Response
    """
    try:
        tp = request.args.get("type")
        code = id
        doc_ref = voucher_ref.document(code)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if tp == "info":
                return jsonify({'success': True, 'data': data}), 200
            elif tp == "image":
                voucher = Voucher.from_dict(data)
                return jsonify({'success': True, 'data': voucher.generate_voucher_image()}), 200
        else:
            abort(404, description=RESOURCE_NOT_FOUND.format(code))
    except NotFoundError as e:
        abort(e.code, description=e)
    except FirebaseError as e:
        abort(e.code, description=e)


@voucher_bp.route('/voucher/redeemed/<id>', methods=["PUT"])
def set_voucher_to_redeemed(id):
    """
    Set voucher to redeemed via the voucher code
    :return: json object
    """
    try:
        code = id
        redeemed = request.get_json()['data']['redeemed']
        doc_ref = voucher_ref.document(code)
        if redeemed:
            doc_ref.set({u'redeemed': redeemed, u'redeemed_on': datetime.today().strftime(date_format)}, merge=True)
        else:
            doc_ref.set({u'redeemed': redeemed, u'redeemed_on': None}, merge=True)
        doc = doc_ref.get()
        data = doc.to_dict()
        return jsonify({'success': True, 'data': data}), 200
    except NotFoundError as e:
        abort(e.code, description=e)
    except FirebaseError as e:
        abort(e.code, description=e)