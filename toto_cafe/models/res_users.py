# _*_ coding: utf-8 _*_
from odoo import models, fields, api
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    def unlink(self):
        for user in self:
            if user.has_group("base.user_admin"):
                raise UserError("请不要删除管理员用户账号。")
        return super().unlink()
