from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CheckInOut(models.Model):
    _name = "check.in.out"
    _description = "Check In/Out"

    name = fields.Many2one(
        'res.users',
        string="Employee Name",
        required=True,
        default=lambda self: self.env.user
    )
    state = fields.Selection(
        [("check in", "Check In"), ("check out", "Check Out")],
        string="Status",
        default="check in"
    )
    date = fields.Datetime(
        string="Date & Time",
        default=fields.Datetime.now,
        required=True
    )
    attachment = fields.Binary(string="Attachment (Photo)")
    sale_order_id = fields.Many2one(
        'sale.order',  # Related model
        string="Related Sale Order",
        ondelete='cascade'
    )
