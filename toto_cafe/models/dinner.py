# _*_ coding: utf-8 _*_
from odoo import models, fields, api


class TotoCafeDinner(models.Model):
    _name = "toto_cafe.dinner"

    type = fields.Selection([
        ("a", "A"),
        ("b", "B"),
    ], required=True, string="Type")
    date = fields.Date(default=fields.Date.today)
    quantity = fields.Integer(default=400)
    image = fields.Image()
    record_ids = fields.One2many("toto_cafe.dinner.record", "dinner_id", string="记录", readonly=True)
    remain = fields.Integer(compute="_compute_remain", store=True, string="剩余餐数")

    _sql_constraints = [
        ('remain_constraint', 'check (remain>=0)', '当前餐已经没有剩余'),
        ('date_type_constraint', 'unique(date, type)', '一天内只能有一次A餐或B餐')
    ]

    def name_get(self):
        return [(dinner.id, '%s %s餐' % (dinner.date, dict(dinner._fields["type"].selection)[dinner.type]))
                for dinner in self]

    @api.depends("record_ids")
    def _compute_remain(self):
        for dinner in self:
            dinner.remain = dinner.quantity - len(dinner.record_ids)

    def add_record(self, department="", section="", name="", no=""):
        self.ensure_one()
        if "客人" not in name and \
                self.record_ids.filtered_domain([('name', '=', name)]):
            return "%s 扫码失败。请不要重复扫码。" % name
        self.write({
                "record_ids": [(0, 0, {
                    "department": department,
                    "section": section,
                    "name": name,
                    "no": no
                })]}
            )
        return "%s 扫码成功。" % name


class TotoCafeDinnerRecord(models.Model):
    _name = "toto_cafe.dinner.record"

    dinner_id = fields.Many2one("toto_cafe.dinner", ondelete="cascade")
    type = fields.Selection(related="dinner_id.type", store=True)
    date = fields.Date(related="dinner_id.date", store=True)
    department = fields.Char(string="Department")
    section = fields.Char(string="Section")
    name = fields.Char(string="Name")
    no = fields.Char(string="No.")
