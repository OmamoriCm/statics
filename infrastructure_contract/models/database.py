# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.tools.safe_eval import safe_eval as eval


class database(models.Model):
    _inherit = "infrastructure.database"

    contract_id = fields.Many2one(
        'account.analytic.account',
        string='Contract',
        domain="[('partner_id','child_of',partner_id),('state','=','open')]",
    )
    contract_state = fields.Selection(
        related='contract_id.state',
        string='Contact Status',
    )

    @api.one
    def update_contract_data_from_database(self):
        client = self.get_client()
        localdict = {'client': client}
        for line in self.contract_id.recurring_invoice_line_ids:
            expression = line.product_id.contracted_quantity_expression
            if not expression:
                continue
            eval(
                expression,
                localdict,
                mode="exec",
                nocopy=True)
            result = localdict.get('result', False)
            if result:
                line.db_quantity = result

    @api.one
    def update_remote_contracted_products(self):
        client = self.get_client()
        modules = ['adhoc_modules']
        for module in modules:
            if client.modules(name=module, installed=True) is None:
                raise Warning(_(
                    "You can not Upload a Contract if module '%s' is not "
                    "installed in the database") % (module))
        client.model('support.contract').remote_update_modules_data(True)

    @api.one
    def upload_contract_data(self):
        client = self.get_client()
        modules = ['web_support_client']
        for module in modules:
            if client.modules(name=module, installed=True) is None:
                raise Warning(_(
                    "You can not Upload a Contract if module '%s' is not "
                    "installed in the database") % (module))
        if not self.contract_id:
            raise Warning(
                _("You can not Upload a Contract if not contracted is linked"))
        imp_fields = [
            'id',
            'name',
            'user',
            'database',
            'server_host',
            'contract_id']
        ['self.asd', ]
        commercial_partner = self.contract_id.partner_id.commercial_partner_id

        server_host = self.env['ir.config_parameter'].get_param('web.base.url')

        # search for user related to commercial partner
        user = self.env['res.users'].search([(
            'partner_id', '=', commercial_partner.id)], limit=1)
        if not user:
            user = user.search([(
                'partner_id', 'child_of', commercial_partner.id)], limit=1)
        if not user:
            raise Warning(_(
                "You can not Upload a Contract if there is not user related "
                "to the contract Partner"))
        rows = [[
            'infrastructure_contract.contract_id_%i' % self.contract_id.id,
            self.contract_id.name,
            user.login,
            self._cr.dbname,
            server_host,
            self.contract_id.id,
        ]]
        client.model('support.contract').load(imp_fields, rows)
