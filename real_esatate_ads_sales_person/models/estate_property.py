from odoo import fields, models,api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _inherit = "estate.property"

sales_id = fields.Many2one("res.users", string="Sales Person",required=True)

@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        sales_person_property_ids = self.env[self._name].search_count([("sales_id", "=", vals.get("sales_id"))])
        if sales_person_property_ids >= 2:
            raise ValidationError("Sales person can't have more than two property")
    return super(EstateProperty, self).create(vals_list)