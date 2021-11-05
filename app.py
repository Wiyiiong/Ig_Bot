#  Copyright (c)  Ong Wi Yi .

from flask import Flask

from ClientManagement.API.VoucherAPI import voucher_bp
from ClientManagement.Exception.ExceptionHandler import *

app = Flask(__name__)
app.register_error_handler(400, handle_bad_request_error)
app.register_error_handler(401, handle_unauthorized_error)
app.register_error_handler(403, handle_forbidden_error)
app.register_error_handler(404, handle_not_found_error)
app.register_error_handler(405, handle_method_not_allowed_error)
app.register_error_handler(500, handle_unexpected_error)
app.register_error_handler(503, handle_service_error)

app.register_blueprint(voucher_bp)
app.register_blueprint(errors_bp)

if __name__ == '__main__':
    app.run(debug=True)