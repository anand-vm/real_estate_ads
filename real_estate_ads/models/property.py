from odoo import fields, models,api

class Property(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread", "mail.activity.mixin", 'utm.mixin'] 
    _description = "Real Estate Property"


    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('accepted', 'Accepted'),
         ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        string="Status", default="new")
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", tracking=True)
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_price") # Accept by self._compute_best_offer or Keep the Methods above the code in an organized way. (Not in between model fields)
    selling_price = fields.Float(string="Selling Price", readonly=True, tracking=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",default="north")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    sales_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain="[('is_company', '=', True)]")
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    # @api.depends("living_area", "garden_area")
    # def _compute_total_area(self):
    #     for record in self:
    #         record.total_area = record.living_area + record.garden_area

    @api.onchange("living_area", "garden_area")
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    total_area = fields.Integer(string="Total Area") #compute="_compute_total_area"


    def action_sold(self):
        self.state = "sold"

    def action_cancelled(self):
        self.state = "cancelled"

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    offer_count = fields.Integer(string="Offer count", compute="_compute_offer_count")


    def action_property_view_offer(self):
        self.ensure_one()  # Ensure the action is called on a single record
        return {
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "tree,form",
            "domain": [("property_id", "=", self.id)],
            "name": f"{self.name} - Offers",
            "context": {"default_property_id": self.id},
        }
    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0


    def action_client_action(self):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "tag": "custom_client_action",
            "params": {"property_id": self.id},
        }

    def action_url_action(self):
        return {
            'type' : 'ir.actions.act_url',
            'url' : "https://www.google.com",
            'domain': [('property_id', '=', self.id)],
            'target': 'self',   # new for open in new tab
        }


    def _get_report_base_filename(self):
        self.ensure_one()
        return "Estate Property - %s" % (self.name)
    

    def action_send_email(self):
        mail_template = self.env.ref('real_estate_ads.offer_mail_template')


    def _get_emails(self):
        return ','.join(self.offer_ids.mapped("partner_id.email"))


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")  # Add the color field