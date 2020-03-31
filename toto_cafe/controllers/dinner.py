# _*_ coding: utf-8 _*_
import json
import base64
from odoo import http, tools
from odoo import models, fields, api


class Dinner(http.Controller):
    @http.route("/dinner", type='http', auth="none", methods=['GET'])
    def dinner(self, with_image=False):
        dinners = http.request.env["toto_cafe.dinner"].sudo().search([
            ("date", "=", fields.Date.today())
        ])
        return json.dumps([{"date": fields.Date.to_string(dinner.date),
                            "type": dinner.type,
                            "quantity": dinner.quantity,
                            "remain": dinner.remain,
                            "image": dinner.image.decode() if with_image and dinner.image else "",
                            } for dinner in dinners])

    @http.route("/dinner", type='http', auth="none", methods=['POST'], csrf=False)
    def dinner_take(self, dinner_type, department="", section="", name="", no=""):
        dinner = http.request.env["toto_cafe.dinner"].sudo().search([
            ("date", "=", fields.Date.today()),
            ("type", "=", dinner_type)
        ])
        user = http.request.env.ref("base.user_admin")
        if dinner:
            return json.dumps(dinner.with_user(user).add_record(department, section, name, no))
