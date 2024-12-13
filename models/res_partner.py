from odoo.exceptions import ValidationError
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    latitude = fields.Float(string="Latitude",digits=(2, 4))
    longitude = fields.Float(string="Longitude",digits=(2, 4))

    def action_view_map(self):
        for record in self:
            if record.latitude and record.longitude:
                map_url = f"https://www.google.com/maps?q={record.latitude},{record.longitude}"
                return {
                    'type': 'ir.actions.act_url',
                    'url': map_url,
                    'target': 'new',
                }
            else:
                raise ValidationError("Please enter valid latitude and longitude values.")
