# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class HrReimbursementAnalysis(models.Model):
    _name = "hr.reimbursement_analysis"
    _description = "Employee Reimbursement Analysis"
    _auto = False

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
    )
    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="hr.employee",
    )
    job_id = fields.Many2one(
        string="Job",
        comodel_name="hr.job",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.company",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.reimbursement_type",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    date_expense = fields.Date(
        string="Date Expense",
    )
    date_due = fields.Date(
        string="Date Due",
    )
    quantity = fields.Float(
        string="Quantity",
    )
    approve_quantity = fields.Float(
        string="Approved Quantity",
    )
    price_unit = fields.Float(
        string="Price Unit",
    )
    approve_price_unit = fields.Float(
        string="Approved Price Unit",
    )
    price_subtotal = fields.Float(
        string="Price Subtotal",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Waiting for Payment"),
            ("done", "Done"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
    )

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            b.company_id AS company_id,
            b.employee_id AS employee_id,
            b.department_id AS department_id,
            b.manager_id AS manager_id,
            b.job_id AS job_id,
            b.type_id AS type_id,
            b.date_expense AS date_expense,
            b.date_due AS date_due,
            a.product_id AS product_id,
            a.quantity AS quantity,
            a.approve_quantity AS approve_quantity,
            a.price_unit AS price_unit,
            a.approve_price_unit AS approve_price_unit,
            a.price_subtotal AS price_subtotal,
            a.analytic_account_id AS analytic_account_id,
            b.state AS state
        """
        return select_str

    def _from(self):
        from_str = """
        hr_reimbursement_line AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN hr_reimbursement AS b ON a.reimbursement_id = b.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
