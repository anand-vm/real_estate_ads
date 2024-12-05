from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError



class AbstractOffer(models.AbstractModel):
    _name = "abstract.model.offer"
    _description = "Abstract Offer"

    partner_email = fields.Char(string="Email")
    partner_phone = fields.Char(string="Phone")



class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _inherit = ["abstract.model.offer"]


    @api.depends("property_id", "partner_id")
    def _compute_name(self):
        for record in self:
            if record.partner_id and record.property_id:
                record.name = f"{record.property_id.name} - {record.partner_id.name}"
            else:
                record.name = False

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')],
        string="Status", default="pending")
    partner_id = fields.Many2one("res.partner", string="Customer")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)


    create_date = fields.Date(string="Created Date", default=fields.Date.context_today)

    # SQL constraints will work only if the field is stored and act before python constraints.
    ''' 
    _sql_constraints = [
        ('validity', 'CHECK(validity > 0)', 'Validity must be strictly positive.'),
    ]
    '''

    @api.depends("create_date", "validity")
    # @api.depends_context('uid')
    def _compute_date_deadline(self):
        """Compute the deadline date based on the create_date and validity."""
        # print(self.env.context)
        # print(self._context)
        for rec in self:
            if rec.create_date and rec.validity:
                rec.date_deadline = rec.create_date + timedelta(days=rec.validity)
            else:
                rec.date_deadline = None

    def _inverse_date_deadline(self):
        """Inverse method to update validity based on create_date and date_deadline."""
        for rec in self:
            if rec.date_deadline and rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date).days
            else:
                rec.validity = None

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set default create_date."""
        for vals in vals_list:
            if not vals.get("create_date"):
                vals['create_date'] = fields.Date.context_today(self)
        return super(PropertyOffer, self).create(vals_list)

    @api.constrains('validity')
    def _check_validity(self):
        """Constraint to ensure validity is greater than 0."""
        for rec in self:
            if rec.date_deadline <= rec.create_date:
                raise ValidationError("Deadline must be greater than create date.")
            
    # ORM Methods - a Lots of examples available in the documentation
    def write(self,vals):
        res_partner_id =  self.env['res.partner'].browse(1)  # Access the partner record
        #res_partner_id =  self.env['res.partner'].search([('is_company', '=', True)])  # Search for a partner record
        # print(res_partner_id.name)
        # print(self.env.uid) # User ID
        # print(self.env.cr) # Cursor ID
        # print(self.env.context) # Context
        # print(vals) # See all values in seld
        return super(PropertyOffer, self).write(vals)
    

    def action_accept_offer(self):
        # self._validate_accepted_offer()  # Call the validation method
        if self.property_id:
            self.property_id.selling_price = self.price
            self.property_id.write({
                'selling_price': self.price,
                'buyer_id': self.partner_id.id,
                'state': 'accepted'
            })
        self.status = "accepted"

    def action_refuse_offer(self):
        self.status = "refused"
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price':0,
                'state': 'offer_received'
            })


    # Find accepted offer for a property and raise an error if there is already an accepted offer
    @api.constrains('status')
    def _validate_accepted_offer(self):
        for record in self:
            if record.status == 'accepted':
                # Check for other accepted offers for the same property
                existing_offers = self.env['estate.property.offer'].search([
                    ('property_id', '=', record.property_id.id),
                    ('status', '=', 'accepted'),
                    ('id', '!=', record.id)  # Exclude the current record
                ])
                if existing_offers:
                    raise ValidationError(
                        "There is already an accepted offer for this property. "
                        "You cannot accept multiple offers for the same property."
                    )
                
    def extend_offer_deadline(self):
        active_ids = self._context.get('active_ids', [])
        if active_ids:
            offer_ids = self.env['estate.property.offer'].browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10

    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity = offer.validity + 1
            
    
# Different types of Models in Odoo
# 1. Standard Model, 2. Abstract Model, 3. Transient Model, 4. Proxy Model, 
# 5. Tree Model, 6. Search Model, 7. Constraint Model,


