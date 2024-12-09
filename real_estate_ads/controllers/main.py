from odoo import http
from odoo.http import request


class PropertyController(http.Controller):
    @http.route('/properties', type='http', auth='public', website=True, methods=['GET'], cors="**", csrf=True)
    def list_properties(self, **kwargs):
        properties = request.env['estate.property'].sudo().search([])
        print("Properties :", properties)
        return request.render('real_estate_ads.property_list_web', {'properties': properties})
