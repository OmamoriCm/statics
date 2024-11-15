# -*- coding: utf-8 -*-
import openerp
from openerp import api, models
from openerp import SUPERUSER_ID
from openerp.exceptions import Warning

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        res = super(MailComposeMessage, self).default_get(fields)
        context = self.env.context
        token = server_url = partner = ''
        ICPSudo = self.env['ir.config_parameter'].sudo()
        PartnerSudo = self.env['res.partner'].sudo()
        UserSudo = self.env['res.users'].sudo()
        CompanySudo = self.env['res.company'].sudo()
        company = CompanySudo.search([], limit=1,  order='id asc')
        if context.get('odoomigrationexperts', False) and context.get('active_model', False) == 'base.config.settings':
            active_model = 'base.config.settings'
            active_id = context.get('active_id')

            server_url = ICPSudo.get_param('web.base.url')
            if active_id:
                token = self.env['base.config.settings'].browse(active_id).migrationexpoerts_token
                if not token:
                    raise Warning("Please generate a Token before sending an email!")
            partner = PartnerSudo.search([('email', '=', 'info@openerpmigrationexperts.com')], limit=1)
            if not partner:
                partner = PartnerSudo.create({'name': 'openerpMigrationExperts.com',
                                              'email': 'info@openerpmigrationexperts.com',
                                              'is_supplier': True})
        if partner:
            superuser= UserSudo.search([('id','=',SUPERUSER_ID)])
            body = '''
            <p>Hello openerpMigrationExperts,</p>
            <p>As per the instructions we have generated the token and would like to share the following information&nbsp;with you to start the database migration process .</p>
            <ul>
            <li style="font-size: 14px;"><strong>Server URL: </strong>%s</li>
            <li style="font-size: 14px;"><strong>Database Name:&nbsp;</strong>%s</li>
            <li style="font-size: 14px;"><strong>SuperUser Login: </strong>%s</li>
            <li style="font-size: 14px;"><strong>openerpMigrationExpert Token: </strong>%s</li>
            <li style="font-size: 14px;"><strong>Current openerp Version: </strong> %s</li>
            <li style="font-size: 14px;"><strong>Target openerp Version: </strong> </li>
            <li style="font-size: 14px;"><strong>Contact Email: </strong> %s</li>
            <li style="font-size: 14px;"><strong>Contact Number: </strong> %s</li>
            <li style="font-size: 14px;"><strong>Any further Queries?: </strong> </li>
            </ul>
            <p>Thank you.</p>
            
            ''' %(server_url, self.env.cr.dbname,superuser.login, token, openerp.release.version,company.phone, company.email)
            res['partner_ids'] = [(6, 0, [partner.id])]
            res['subject'] = 'openerpMigrationExperts Database Migration'
            res['body'] = body
        return res
