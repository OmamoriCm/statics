# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date

from openerp.tests.common import TransactionCase


class TestWorkflow(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(TestWorkflow, self).setUp(*args, **kwargs)
        return result

    def _create_no_error(self):

        self.env.ref("hr.employee_al").write(
            {
                "address_home_id": self.env.ref("base.res_partner_2").id,
            }
        )
        values = {
            "employee_id": self.env.ref("hr.employee_al").id,
            "type_id": self.env.ref("hr_reimbursement.demo_reimbursement_type01").id,
            "date_expense": date.today().strftime("%Y-%m-%d"),
            "date_due": date.today().strftime("%Y-%m-%d"),
        }
        rec_cache = self.env["hr.reimbursement"].new(values)
        rec_cache.onchange_journal_id()
        rec_cache.onchange_department_id()
        rec_cache.onchange_manager_id()
        rec_cache.onchange_job_id()
        rec_cache.onchange_employee_reimbursement_payable_account_id()
        values = rec_cache._convert_to_write(rec_cache._cache)
        reimbursement = self.env["hr.reimbursement"].create(values)
        detail_cache = self.env["hr.reimbursement_line"].new(
            {
                "reimbursement_id": reimbursement.id,
                "product_id": self.env.ref("product.product_product_4").id,
                "price_unit": 800.00,
                "company_id": self.env["hr.reimbursement"]._default_company_id(),
                "currency_id": self.env["hr.reimbursement"]._default_currency_id(),
            }
        )
        detail_cache.onchange_uom_id()
        detail_cache.onchange_approve_quantity()
        detail_cache.onchange_approve_price_unit()
        detail_cache.onchange_account_id()
        detail_values = detail_cache._convert_to_write(detail_cache._cache)
        self.env["hr.reimbursement_line"].create(detail_values)
        self.assertEqual(reimbursement.state, "draft")
        return reimbursement

    def action_confirm_no_error(self, reimbursement):
        reimbursement.action_confirm()
        self.assertEqual(reimbursement.state, "confirm")

    def action_approve_no_error(self, reimbursement):
        reimbursement.restart_validation()
        self.assertEqual(
            reimbursement.definition_id.name, "Employee Reimbursement - (test)"
        )
        reimbursement.invalidate_cache()
        reimbursement.validate_tier()
        self.assertTrue(reimbursement.validated)
        self.assertEqual(reimbursement.state, "approve")

    def test_1(self):
        reimbursement = self._create_no_error()
        self.action_confirm_no_error(reimbursement)
        self.action_approve_no_error(reimbursement)
