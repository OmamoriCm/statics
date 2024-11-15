from openerp import models, api


class MultiPaySlipWiz(models.TransientModel):
    _name = 'multi.pay.slip.wiz'

    @api.multi
    def confirm_multi_pay_slip(self):
        payslip_ids = self.env['hr.payslip'].browse(self._context.get(
                'active_ids'))
        for payslip in payslip_ids:
            if payslip.state == 'draft':
                if payslip.hr_verify_sheet():
                    payslip.process_sheet()

