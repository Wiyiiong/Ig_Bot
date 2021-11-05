#  Copyright (c)  Ong Wi Yi .
import base64
import configparser
import io
from datetime import datetime, timedelta
from enum import Enum

from PIL import Image, ImageDraw, ImageFont

from ClientManagement.Util.VoucherCodeGenerator import VoucherCodeGenerator

config = configparser.ConfigParser()
config.read("config.ini")

date_format = "%d %b %Y"


class VoucherType(Enum):
    SEASONAL_PROMO = 1
    NEW_CUSTOMER = 2
    LIFETIME_PROMO = 3


class Voucher:
    """
    Voucher Class that creates voucher for the customer
    """

    def __init__(self, voucher_type, value, valid_duration: int, name, redeemed_on=None, redeemed=False,
                 release_date=datetime.today(), code=VoucherCodeGenerator.generate_code()):
        self.voucher_type = voucher_type
        self.value = value
        self.valid_duration = valid_duration
        self.name = name
        self.redeemed_on = redeemed_on
        self.redeemed = redeemed
        self.release_date = release_date
        self.code = code

    # Retrieve voucher expiry date
    def get_expiry_date(self):
        expiry_date = self.release_date + timedelta(days=self.valid_duration)
        return expiry_date.strftime(date_format).upper()

    # Generate voucher image
    def generate_voucher_image(self):
        template_path = config["VOUCHER_CONFIG"]["voucher_template_path"]
        value_font_path = config["VOUCHER_CONFIG"]["value_font_path"]
        code_font_path = config["VOUCHER_CONFIG"]["code_font_path"]
        date_font_path = config["VOUCHER_CONFIG"]["date_font_path"]
        value_font = ImageFont.truetype(value_font_path, size=120)
        code_font = ImageFont.truetype(code_font_path, size=50)
        date_font = ImageFont.truetype(date_font_path, size=45)
        color = "#" + config["VOUCHER_CONFIG"]["font_color"]
        value_font_color = "#" + config["VOUCHER_CONFIG"]["value_font_color"]
        template = Image.open(template_path)
        print(template.size)

        draw = ImageDraw.Draw(template)
        draw.text((1730, 350), self.value, font=value_font, fill=value_font_color, align="center")
        draw.text((1800, 580), self.code, font=code_font, fill=color, align="center")
        draw.text((2110, 1190), self.get_expiry_date(), font=date_font, fill=color, align="center")

        buff = io.BytesIO()
        template.save(buff, format='JPEG')
        base64_img = base64.b64encode(buff.getvalue())

        return str(base64_img)

    @staticmethod
    def from_dict(source):
        voucher = Voucher(source['voucher_type'], source['value'], int(source['valid_duration']), source['name'])
        if 'redeemed_on' in source:
            voucher.redeemed_on = source['redeemed_on']
        if 'redeemed' in source:
            voucher.redeemed = source['redeemed']
        if 'release_date' in source:
            voucher.release_date = datetime.strptime(source['release_date'], date_format)
        if 'code' in source:
            voucher.code = source['code']
        return voucher

    def to_dict(self):
        dict = {'voucher_type': self.voucher_type, 'value': self.value, 'valid_duration': self.valid_duration,
                'name': self.name}
        if self.redeemed_on:
            dict['redeemed_on'] = self.redeemed_on
        if self.redeemed:
            dict['redeemed'] = self.redeemed
        if self.release_date:
            dict['release_date'] = self.release_date.strftime(date_format)
        if self.code:
            dict['code'] = self.code

        return dict

    def __repr__(self):
        return (f'Voucher(\
                voucher_type={self.voucher_type}, \
                value={self.value}, \
                valid_duration={self.valid_duration}, \
                name={self.name}, \
                redeemed_on={self.redeemed_on}, \
                redeemed={self.redeemed}, \
                release_date={self.release_date}, \
                code ={self.code} \
               )')