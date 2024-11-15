from openerp import models, fields, api
import random
import string

class OdooMigrationExpertsConfig(models.TransientModel):
    _inherit = 'base.config.settings'


    migrationexpoerts_token = fields.Char('OdooMigrationExperts TOKEN')

    @api.multi
    def generate_token(self):
        return self.set_migrationexpoerts_token()

    @api.multi
    def set_migrationexpoerts_token(self):
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        self.migrationexpoerts_token = token
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("tko_odoomigrationexperts_client.token", token)

    @api.multi
    def get_migrationexpoerts_token(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        return {'migrationexpoerts_token': ICPSudo.get_param('tko_odoomigrationexperts_client.token')}

