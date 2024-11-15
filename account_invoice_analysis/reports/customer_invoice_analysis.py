# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class CustomerInvoiceAnalysis(models.Model):
    _name = "account.customer_invoice_analysis"
    _description = "Customer Invoice Analysis"
    _auto = False

    date_invoice = fields.Date(
        string="Date Invoice",
    )
    product_id = fields.Many2one(
        string="product.product",
        comodel_name="product.product",
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="account.payment.term",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="account.period",
    )
    product_categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    commercial_partner_id = fields.Many2one(
        string="Commercial Partner",
        comodel_name="res.partner",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ("out_invoice", "Customer Invoice"),
            ("in_invoice", "Supplier Invoice"),
            ("out_refund", "Customer Refund"),
            ("in_refund", "Supplier Refund"),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("proforma", "Pro-forma"),
            ("proforma2", "Pro-forma"),
            ("open", "Open"),
            ("paid", "Done"),
            ("cancel", "Cancelled"),
        ],
    )
    date_due = fields.Date(string="Date Due,")
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    account_analytic_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    partner_bank_id = fields.Many2one(
        string="Partner Bank",
        comodel_name="res.partner.bank",
    )
    country_id = fields.Many2one(
        string="Country",
        comodel_name="res.country",
    )
    product_qty = fields.Float(
        string="Qty",
    )
    price_total = fields.Float(
        string="Total Without Tax",
    )
    price_average = fields.Float(
        string="Average Price",
    )
    residual = fields.Float(
        string="Residual",
    )
    nbr = fields.Integer(
        string="# Line",
    )

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            a.date AS date_invoice,
            a.product_id AS product_id,
            a.payment_term AS payment_term_id,
            a.period_id AS period_id,
            a.currency_id AS currency_id,
            a.categ_id AS product_categ_id,
            a.journal_id AS journal_id,
            a.partner_id AS partner_id,
            a.commercial_partner_id AS commercial_partner_id,
            a.company_id AS company_id,
            a.user_id AS user_id,
            a.type AS type,
            a.state AS state,
            a.date_due AS date_due,
            a.account_id AS account_id,
            b.account_analytic_id AS account_analytic_id,
            a.partner_bank_id AS partner_bank_id,
            a.country_id AS country_id,
            SUM(a.product_qty) AS product_qty,
            SUM(a.price_total) AS price_total,
            SUM(a.price_average) AS price_average,
            SUM(a.residual) AS residual,
            COUNT(a.id) AS nbr
        """
        return select_str

    def _from(self):
        from_str = """
        account_invoice_report AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1 AND
            (a.type = 'out_invoice' OR a.type = 'out_refund')
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN account_invoice_line AS b ON a.id = b.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY
            a.id,
            a.date,
            a.product_id,
            a.payment_term,
            a.period_id,
            a.currency_id,
            a.categ_id,
            a.journal_id,
            a.partner_id,
            a.commercial_partner_id,
            a.company_id,
            a.user_id,
            a.type,
            a.state,
            a.date_due,
            a.account_id,
            b.account_analytic_id,
            a.partner_bank_id,
            a.country_id
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
