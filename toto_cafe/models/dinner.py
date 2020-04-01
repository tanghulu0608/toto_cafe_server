# _*_ coding: utf-8 _*_
from odoo import models, fields, api


class TotoCafeDinner(models.Model):
    _name = "toto_cafe.dinner"
    _order = "date desc, type"
    type = fields.Selection([
        ("a", "A"),
        ("b", "B"),
    ], required=True, string="类型")
    date = fields.Date(default=fields.Date.today, string="日期")
    quantity = fields.Integer(default=400, string="数量")
    image = fields.Image(string="图片")
    record_ids = fields.One2many("toto_cafe.dinner.record", "dinner_id", string="记录", readonly=False)
    remain = fields.Integer(compute="_compute_remain", store=True, string="剩余餐数")

    _sql_constraints = [
        ('date_type_constraint', 'unique(date, type)', '一天内只能有一次A餐或B餐')
    ]

    def name_get(self):
        return [(dinner.id, '%s %s餐' % (dinner.date, dict(dinner._fields["type"].selection)[dinner.type]))
                for dinner in self]

    @api.depends("quantity", "record_ids")
    def _compute_remain(self):
        for dinner in self:
            dinner.remain = dinner.quantity - len(dinner.record_ids)

    def add_record(self, department="", section="", name="", no=""):
        self.ensure_one()
        res = {
            "error": 0,
            "msg": "",
            "remain": 0
        }
        if self.remain <= 0:
            res["error"] = 1
            res["msg"] = "当前餐已经没有剩余"
            return res
        self.write({"record_ids": [(0, 0, {
            "department": department,
            "section": section,
            "name": name,
            "no": no
        })]})
        self.flush()
        res["msg"] = "%s 扫码成功。" % name
        res["remain"] = self.remain
        return res


class TotoCafeDinnerRecord(models.Model):
    _name = "toto_cafe.dinner.record"
    _order = "create_date"

    dinner_id = fields.Many2one("toto_cafe.dinner", ondelete="cascade")
    type = fields.Selection(related="dinner_id.type", store=True)
    date = fields.Date(related="dinner_id.date", store=True)
    department = fields.Char(string="部门")
    section = fields.Char(string="课室")
    name = fields.Char(string="姓名")
    no = fields.Char(string="工号")
