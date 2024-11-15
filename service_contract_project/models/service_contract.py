# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = "service.contract"

    auto_create_project_ok = fields.Boolean(
        string="Auto Create Project",
        default=False,
    )
    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )

    @api.multi
    def action_approve(self):
        _super = super(ServiceContract, self)
        _super.action_approve()
        for record in self:
            record._create_project()

    @api.onchange(
        "type_id",
    )
    def onchange_auto_create_project_ok(self):
        self.auto_create_project_ok = False
        if self.type_id:
            self.auto_create_project_ok = self.type_id.auto_create_project_ok

    @api.multi
    def _create_project(self):
        self.ensure_one()
        if self.auto_create_project_ok and not self.project_id:
            project = self.env["project.project"].create(self._prepare_project())
            self.write(
                {
                    "project_id": project.id,
                    "user_id": self.responsible_id.id,
                }
            )

    @api.multi
    def _prepare_project(self):
        self.ensure_one()
        return {
            "analytic_account_id": self.analytic_account_id.id,
        }
