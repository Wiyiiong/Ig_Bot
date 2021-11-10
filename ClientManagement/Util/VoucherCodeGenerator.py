#  Copyright (c)  Ong Wi Yi .

import configparser

import rstr


class VoucherCodeGenerator:
    """
    Generate random voucher code
    """

    @staticmethod
    def generate_code(code_list: []):
        config = configparser.ConfigParser()
        config.read("config.ini")
        length = int(config["VOUCHER_CONFIG"]["length"])
        alphabet_length = length // 2
        code = rstr.xeger("[A-Z]{" + str(length // 2) + "}\d{" + str(alphabet_length) + "}")
        if code in code_list:
            VoucherCodeGenerator.generate_code(code_list)
        return code