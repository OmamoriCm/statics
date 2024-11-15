# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class ResPartner(models.Model):
    """Add legal_name"""

    _inherit = "res.partner"

    @api.depends(
        "manual_legal_name",
        "name",
    )
    def _compute_legal_name(self):
        for record in self:
            legal_name = record.name
            if record.manual_legal_name:
                legal_name = record.manual_legal_name
            record.legal_name = legal_name

    manual_legal_name = fields.Char(
        string="Manual Legal Name",
        required=False,
    )
    legal_name = fields.Char(
        string="Legal Name", compute="_compute_legal_name", required=False, store=False
    )
