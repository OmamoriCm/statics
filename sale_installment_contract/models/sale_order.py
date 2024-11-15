from dateutil.relativedelta import relativedelta
import datetime

from openerp.osv import osv, fields, orm
from openerp import models, api
from openerp.tools.translate import _
from logging import getLogger
from openerp.exceptions import ValidationError

_logger = getLogger(__name__)


class sale_order(osv.osv):

    _inherit = 'sale.order'

    _columns = {
        'installment_sale': fields.boolean('Installments mode', readonly=True,
            states={'draft': [('readonly', False)],},
            help='Generate installments from contract linked to this order'),
        'down_payment_amount': fields.float('Initial/down payment amount', readonly=True,
            states={'draft': [('readonly', False)],},
            help='default is percentage, if fixed check the fixed amount box' ),
        'down_payment_fixed': fields.boolean('Fixed amount', readonly=True,
            states={'draft': [('readonly', False)],}),
        'installments_count': fields.integer('Number of installments', readonly=True,
            states={'draft': [('readonly', False)],}),
        'installment_amount': fields.float('Installment amount', readonly=True),
        'recurring_rule_type': fields.selection([
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)'),
            ], 'Recurrency', readonly=True,
                states={'draft': [('readonly', False)],},
                help="Installments automatically repeat at specified interval"),
        'recurring_interval': fields.integer('Repeat Every', readonly=True,
            states={'draft': [('readonly', False)],},
            help="Repeat every (Days/Week/Month/Year)"),
        'recurring_next_date': fields.date('Date of Next Installment', readonly=True,
            states={'draft': [('readonly', False)],}),
    }

    @api.multi
    @api.constrains('installments_count','recurring_interval','down_payment_fixed')
    def _check_constrains(self):
        if self.installment_sale:
            if  self.installments_count < 3:
                raise ValidationError("Number of Installments must be more than 2")
            if self.recurring_interval < 1:
                raise ValidationError("Repeat every should be 1 or more")
            if not self.down_payment_fixed and self.down_payment_amount > 80:
                raise ValidationError("Percent payment can not exceed 80%")

    def action_button_confirm(self, cr, uid, ids, context=None):
        super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
        # _logger.warning('Order Ids %s', ids)
        # we need to get the order which is linked to our contract
        for order in self.browse(cr, uid, ids, context=context):
            order._check_constrains()

            if order.installment_sale:
                # Calc the installment_amount
                if order.down_payment_fixed:
                    order.installment_amount = (order.amount_total - order.down_payment_amount) / order.installments_count
                else:
                    # if not fixed amount then
                    # installment = (total - (total *(down_payment/100))) / installments_count
                    order.installment_amount = (order.amount_total - (order.amount_total * (order.down_payment_amount / 100))) / order.installments_count

                # calc contract end date
                interval = order.recurring_interval
                next_date = datetime.datetime.strptime(order.recurring_next_date or current_date, "%Y-%m-%d")
                if order.recurring_rule_type == 'daily':
                    date_end = next_date+relativedelta(days=+(interval*(order.installments_count-1)))
                elif order.recurring_rule_type == 'weekly':
                    date_end = next_date+relativedelta(weeks=+(interval*(order.installments_count-1)))
                elif order.recurring_rule_type == 'monthly':
                    date_end = next_date+relativedelta(months=+(interval*(order.installments_count-1)))
                else:
                    date_end = next_date+relativedelta(years=+(interval*(order.installments_count-1)))

                # Contract creation values
                vals = {
                    'type': 'contract',
                    'name': order.order_line[0].name + ' ' + order.partner_id.name,
                    'code': order.order_line[0].name + ' ' + order.partner_id.name,
                    'user_id': order.user_id.id,
                    'partner_id': order.partner_id.id,
                    'date_start': order.recurring_next_date,
                    'date': date_end,
                    'recurring_interval': order.recurring_interval,
                    'recurring_rule_type': order.recurring_rule_type,
                    'recurring_next_date': order.recurring_next_date,
                    'recurring_invoices': 1,
                    'installment_mode': 1,
                    'auto_confirm_invoices': 1,
                    'fix_price_invoices': 1,
                    }

                # use linked contract or create new one
                if order.project_id:
                    contract_obj = order.project_id
                    contract_id = contract_obj.id
                    contract_obj.write(vals)
                else:
                    contract_model = self.pool['account.analytic.account']
                    contract_id = contract_model.create(cr, uid, vals, context=context)
                    contract_obj = self.pool['account.analytic.account'].browse(cr, uid, contract_id, context=context)
                    order.write({'project_id':contract_id,})

                # invoice lines
                line_ids = []
                for line in order.order_line:
                    line_vals = {
                        'analytic_account_id': contract_id,
                        'product_id': line.product_id.id,
                        'name': line.name + ' installment',
                        'quantity': line.product_uom_qty,
                        'uom_id': line.product_uom.id,
                        'price_unit': order.installment_amount and order.installment_amount or 0.0,
                    }
                    inv_line = self.pool['account.analytic.invoice.line'].create(cr, uid, line_vals, context=context)
                    line_ids.append(inv_line)

                if contract_id:
                    inv_lines = self.pool['account.analytic.invoice.line'].browse(cr, uid, line_ids, context=context)
                    contract_obj.recurring_invoice_line_ids += inv_lines

                if order.down_payment_amount > 0 :
                    # Generate advance payment invocie
                    inv_vals = {
                        'partner_id': order.partner_id.id ,
                        'account_id': order.partner_invoice_id.property_account_receivable.id ,
                        'company_id': order.company_id.id ,
                        'currency_id': order.currency_id.id ,
                        'journal_id':  self.pool['account.invoice'].default_get(cr, uid, ['journal_id'], context=context)['journal_id'],
                        'type': 'out_invoice',
                    }
                    # create invocie
                    inv_id = self.pool['account.invoice'].create(cr, uid, inv_vals, context=context)
                    inv_obj = self.pool['account.invoice'].browse(cr, uid, inv_id, context=context)
                    # Add invoice id to order.invoice_ids
                    order.invoice_ids += inv_obj

                    #calc down_payment
                    if order.down_payment_fixed:
                        down_pay = order.down_payment_amount
                    else:
                        down_pay = order.amount_total * (order.down_payment_amount / 100)

                    # Generate advance invoice line
                    percent_simpol = order.down_payment_fixed and '.' or ' %'
                    l_vals = {
                        'account_analytic_id': contract_id,
                        'name':  order.partner_invoice_id.name + ' ' + order.order_line[0].name + ' Down/Advance Payment ' + str(order.down_payment_amount) + percent_simpol,
                        'quantity': order.order_line[0].product_uom_qty,
                        'uos_id': order.order_line[0].product_uom.id,
                        'price_unit': down_pay and down_pay or 0.0,
                        'invoice_id': inv_id ,
                    }
                    # create down payment invoice line
                    i_line_id = self.pool['account.invoice.line'].create(cr, uid, l_vals, context=context)
                    i_line_obj = self.pool['account.invoice.line'].browse(cr, uid, i_line_id, context=context)

                    # Link the invoice line and confirm the invoice
                    inv_obj.invoice_line += i_line_obj
                    inv_obj.signal_workflow('invoice_open')

        return True
