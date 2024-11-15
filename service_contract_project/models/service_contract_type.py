# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractType(models.Model):
    _name = "service.contract_type"
    _inherit = "service.contract_type"

    auto_create_project_ok = fields.Boolean(
        string="Auto Create Project",
        default=False,
    )
