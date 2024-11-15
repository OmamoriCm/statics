__author__ = 'tbri'
from openerp import models, fields, api, _

class currency_lookup_wizard(models.TransientModel):
    _name = 'currency_lookup_wizard'

    @api.onchange('currency_date', 'from_currency_id', 'to_currency_id', 'from_amount')
    def calculate(self):
        if not self.from_currency_id or not self.to_currency_id or not self.from_amount or not self.currency_date:
            return
        currency_obj = self.env['res.currency']
        from_currency_at_date = self.from_currency_id.with_context(date=self.currency_date)
        to_currency_at_date = self.to_currency_id.with_context(date=self.currency_date)

        self.to_amount = from_currency_at_date.compute(self.from_amount, to_currency_at_date)
        self.rate_backward = from_currency_at_date.compute(1.00, to_currency_at_date)
        self.rate_forward = to_currency_at_date.compute(1.00, from_currency_at_date)

    currency_date = fields.Date('Date', default=fields.Date.today())
    from_currency_id = fields.Many2one('res.currency', string='From currency', required=True)
    to_currency_id = fields.Many2one('res.currency', string='To currency', required=True)
    from_amount = fields.Float('From amount', required=True)
    to_amount = fields.Float('To amount', readonly=True)

    rate_forward = fields.Float('Forward currency rate', readonly=True)
    rate_backward = fields.Float('Backward currency rate', readonly=True)