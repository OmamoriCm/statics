# -*- coding: utf-8 -*-
##############################################################################
#
#    Education module Odoo 8
#    Copyright (c) 2018 Copyright (c) 2018 aek
#      Anicet Eric Kouame <anicetkeric@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
from openerp import models, fields, api
from ..tools import Number_To_Word


class Voucher(models.Model):
    _inherit = 'account.voucher'

    stamped = fields.Float('Tamped', default=0)
    journal_type = fields.Selection('Journal Type', related='journal_id.type', store=False)
    invoice_id = fields.Integer('Invoice ID')

    @api.multi
    @api.onchange('journal_type')
    def _update_voucher_amount(self):
        self.stamped = 0

    @api.one
    @api.depends('amount')
    def _get_amount_to_letter(self):
        if self.amount:
            self.amount_letter = Number_To_Word.Number_To_Word(self.amount, 'en', self.currency_id.symbol, '')

    amount_letter = fields.Char(compute='_get_amount_to_letter')
