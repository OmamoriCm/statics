# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementTemplateAppendix(models.Model):
    _name = "agreement.template_appendix"
    _inherit = "agreement.appendix_abstract"
    _description = "Agreement Template Appendix"

    agreement_id = fields.Many2one(
        comodel_name="agreement.template",
    )
