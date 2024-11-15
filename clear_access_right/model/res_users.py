from openerp import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def button_clear_access(self):
        self.ensure_one()
        admin_groups = [self.env.ref('base.group_user').id, self.env.ref('base.group_erp_manager').id, self.env.ref('base.group_system').id]
        group_list = []
        for group_id in self.groups_id:
            # Restrict To Clear Admin User Access
            if self.env.uid == self.id and group_id.id in admin_groups:
                continue
            group_list.append((3, group_id.id))
        self.write({'groups_id': group_list})
        return True
