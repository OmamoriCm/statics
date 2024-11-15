# -*- coding: utf-8 -*-

from openerp import models, fields, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    auto_transfer_picking = fields.Boolean(
        string=_('Auto Transfer Picking'),
        help=_(
            "If enabled, when a POS order is validated, the stock picking "
            "will be automatically confirmed and transfered. \n"
            "Otherwise the stock picking will be only confirmed."
        ),
        default=True
    )

    return_picking_type_id = fields.Many2one(
        string=_('Return picking type'),
        comodel_name='stock.picking.type',
    )
