# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import calendar
import logging
from datetime import datetime, time

from dateutil.relativedelta import relativedelta
from openerp import _, api, fields, models, tools
from openerp.addons.decimal_precision import decimal_precision as dp
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)

try:
    import numpy as np
except (ImportError, IOError) as err:
    _logger.debug(err)


class DummyFy(object):
    def __init__(self, *args, **argv):
        for key, arg in argv.items():
            setattr(self, key, arg)


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _description = "Asset"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _order = "date_start desc, name"
    _parent_store = True
    _state_from = ["draft", "confirm"]
    _state_to = ["open", "close"]

    account_move_line_ids = fields.One2many(
        string="Entries",
        comodel_name="account.move.line",
        inverse_name="asset_id",
        readonly=True,
    )

    @api.multi
    @api.depends(
        "depreciation_line_ids",
    )
    def _compute_move_line_check(self):
        for document in self:
            for line in document.depreciation_line_ids:
                if line.move_id:
                    document.move_line_check = True
                else:
                    document.move_line_check = False

    move_line_check = fields.Boolean(
        string="Has accounting entries",
        compute="_compute_move_line_check",
    )

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            if rec.code:
                name = "[{}] {}".format(rec.code, rec.name)
            else:
                name = "%s" % (rec.name)
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        res = super(AccountAssetAsset, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        args = list(args or [])
        if name:
            criteria = ["|", ("code", operator, name), ("name", operator, name)]
            criteria = criteria + args
            asset_ids = self.search(criteria, limit=limit)
            if asset_ids:
                return asset_ids.name_get()
        return res

    name = fields.Char(
        string="Asset Name",
        size=64,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    code = fields.Char(
        string="Reference",
        size=32,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default="/",
        copy=False,
    )
    purchase_value = fields.Float(
        string="Purchase Value",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="\nThe Asset Value is calculated as follows:"
        "\nPurchase Value - Salvage Value.",
    )

    @api.multi
    def _asset_value_compute(self):
        self.ensure_one()
        if self.type == "view":
            asset_value = 0.0
        else:
            asset_value = self.purchase_value - self.salvage_value
        return asset_value

    @api.multi
    def _value_get(self):
        self.ensure_one()
        asset_value = self._asset_value_compute()
        for child in self.child_ids:
            asset_value += (
                child.type == "normal"
                and child._asset_value_compute()
                or child._value_get()
            )
        return asset_value

    @api.model
    def _get_asset_value_field(self):
        return [
            ("+", "purchase_value"),
        ]

    @api.multi
    def _get_asset_value(self):
        """
        Dynamically add/subsstract asset value from list.
        List of fields and their sign will be provided by
        _get_asset_value_field method.
        This will allow modification for other fixed asset event
        (e.g improvement or impairment)
        """
        self.ensure_one()
        result = 0.0
        for field_dict in self._get_asset_value_field():
            if field_dict[0] == "+":
                result += getattr(self, field_dict[1])
            else:
                result -= getattr(self, field_dict[1])
        return result

    @api.multi
    @api.depends(
        "purchase_value",
        "salvage_value",
        "type",
        "method",
        "child_ids",
        "child_ids.asset_value",
        "child_ids.parent_id",
    )
    def _compute_asset_value(self):
        for asset in self:
            if asset.type == "view":
                asset_value = 0.0
                for child in asset.child_ids:
                    if child.state == "open" and child.type == "normal":
                        asset_value += child.asset_value
                asset.asset_value = asset_value
            elif asset.method in ["linear-limit", "degr-limit"]:
                asset.asset_value = asset._get_asset_value()
            else:
                asset.asset_value = asset._get_asset_value()

    asset_value = fields.Float(
        string="Asset Value",
        digits_compute=dp.get_precision("Account"),
        compute=_compute_asset_value,
        store=True,
        help="This amount represent the initial value of the asset.",
    )

    @api.multi
    def _get_additional_depreciated_value(self):
        self.ensure_one()
        result = 0.0
        for field_dict in self._get_additional_depreciated_value_field():
            if field_dict[0] == "+":
                result += getattr(self, field_dict[1])
            else:
                result -= getattr(self, field_dict[1])
        return result

    @api.model
    def _get_additional_depreciated_value_field(self):
        return []

    @api.multi
    @api.depends(
        "asset_value",
        "depreciation_line_ids",
        "depreciation_line_ids.amount",
        "depreciation_line_ids.previous_id",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_id",
        "child_ids",
        "child_ids.value_residual",
        "child_ids.value_depreciated",
        "child_ids.parent_id",
    )
    def _compute_depreciation(self):
        for asset in self:
            if asset.type == "normal":
                lines = asset.depreciation_line_ids.filtered(
                    lambda l: l.type in ("depreciate", "remove")
                    and (l.init_entry or l.move_check)
                )
                value_depreciated = (
                    sum(totl.amount for totl in lines)
                    + asset._get_additional_depreciated_value()
                )
                asset.value_residual = asset._get_asset_value() - value_depreciated
                asset.value_depreciated = value_depreciated
            else:
                value_residual = value_depreciated = 0.0
                for child in asset.child_ids:
                    if child.state == "open" and child.type == "normal":
                        value_residual += child.value_residual
                        value_depreciated += child.value_depreciated
                asset.value_residual = value_residual
                asset.value_depreciated = value_depreciated

    value_residual = fields.Float(
        string="Residual Value",
        digits_compute=dp.get_precision("Account"),
        compute=_compute_depreciation,
        store=True,
    )
    value_depreciated = fields.Float(
        string="Depreciated Value",
        digits_compute=dp.get_precision("Account"),
        compute=_compute_depreciation,
        store=True,
    )
    salvage_value = fields.Float(
        string="Salvage Value",
        digits_compute=dp.get_precision("Account"),
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="The estimated value that an asset will realize upon "
        "its sale at the end of its useful life.\n"
        "This value is used to determine the depreciation amounts.",
    )
    note = fields.Text(
        string="Note",
    )
    category_id = fields.Many2one(
        string="Asset Category",
        comodel_name="account.asset.category",
        change_default=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    parent_id = fields.Many2one(
        string="Parent Asset",
        comodel_name="account.asset.asset",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain=[("type", "=", "view")],
        ondelete="restrict",
    )
    parent_left = fields.Integer(
        string="Parent Left",
        select=1,
    )
    parent_right = fields.Integer(
        string="Parent Right",
        select=1,
    )
    child_ids = fields.One2many(
        string="Child Assets",
        comodel_name="account.asset.asset",
        inverse_name="parent_id",
    )
    date_start = fields.Date(
        string="Asset Start Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=datetime.now().strftime("%Y-%m-%d"),
        help="You should manually add depreciation lines "
        "with the depreciations of previous fiscal years "
        "if the Depreciation Start Date is different from the date "
        "for which accounting entries need to be generated.",
    )
    date_remove = fields.Date(
        string="Asset Removal Date",
        readonly=True,
        copy=False,
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "Running"),
            ("close", "Close"),
            ("removed", "Removed"),
            ("cancel", "Cancelled"),
        ],
        required=True,
        readonly=True,
        copy=False,
        default="draft",
        help="When an asset is created, the status is 'Draft'.\n"
        "If the asset is confirmed, the status goes in 'Running' "
        "and the depreciation lines can be posted "
        "to the accounting.\n"
        "If the last depreciation line is posted, "
        "the asset goes into the 'Close' status.\n"
        "When the removal entries are generated, "
        "the asset goes into the 'Removed' status.",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.multi
    def _get_method(self):
        return self.env["account.asset.category"]._get_method()

    method = fields.Selection(
        string="Computation Method",
        selection=lambda self: self._get_method(),
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default="linear",
        help="Choose the method to use to compute "
        "the amount of depreciation lines.\n"
        "  * Linear: Calculated on basis of: "
        "Gross Value / Number of Depreciations\n"
        "  * Degressive: Calculated on basis of: "
        "Residual Value * Degressive Factor"
        "  * Degressive-Linear (only for Time Method = Year): "
        "Degressive becomes linear when the annual linear "
        "depreciation exceeds the annual degressive depreciation",
    )
    method_number = fields.Integer(
        string="Number of Years",
        readonly=True,
        default=5,
        states={"draft": [("readonly", False)]},
        help="The number of years needed to depreciate your asset",
    )
    method_period = fields.Selection(
        string="Period Length",
        selection=[
            ("month", "Month"),
            ("quarter", "Quarter"),
            ("year", "Year"),
        ],
        required=True,
        readonly=True,
        default="year",
        states={"draft": [("readonly", False)]},
        help="Period length for the depreciation accounting entries",
    )
    method_end = fields.Date(
        string="Ending Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    method_progress_factor = fields.Float(
        string="Degressive Factor",
        readonly=True,
        default=0.3,
        states={"draft": [("readonly", False)]},
    )

    @api.multi
    def _get_method_time(self):
        return self.env["account.asset.category"]._get_method_time()

    method_time = fields.Selection(
        string="Time Method",
        selection=lambda self: self._get_method_time(),
        required=True,
        readonly=True,
        default="year",
        states={"draft": [("readonly", False)]},
        help="Choose the method to use to compute the dates and "
        "number of depreciation lines.\n"
        "  * Number of Years: Specify the number of years "
        "for the depreciation.\n",
    )
    prorata = fields.Boolean(
        string="Prorata Temporis",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Indicates that the first depreciation entry for this asset "
        "have to be done from the depreciation start date instead "
        "of the first day of the fiscal year.",
    )
    history_ids = fields.One2many(
        string="History",
        comodel_name="account.asset.history",
        inverse_name="asset_id",
        readonly=True,
        copy=False,
    )
    depreciation_line_ids = fields.One2many(
        string="Depreciation Lines",
        comodel_name="account.asset.depreciation.line",
        inverse_name="asset_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ("view", "View"),
            ("normal", "Normal"),
        ],
        required=True,
        readonly=True,
        default="normal",
        states={"draft": [("readonly", False)]},
    )

    @api.model
    def _get_company(self):
        obj_res_company = self.env["res.company"]
        return obj_res_company._company_default_get("account.asset.asset")

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        readonly=True,
        default=lambda self: self._get_company(),
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        related="company_id.currency_id",
        readonly=True,
    )
    account_analytic_id = fields.Many2one(
        string="Analytic account",
        comodel_name="account.analytic.account",
        domain=[("type", "!=", "view"), ("state", "not in", ("close", "cancelled"))],
    )

    @api.multi
    def _get_method_time_coefficient(self):
        self.ensure_one()
        result = 0
        if self.method_time == "year":
            result = 12
        elif self.method_time == "month":
            result = 1
        return result

    @api.multi
    def _get_method_period_coefficient(self):
        self.ensure_one()
        return 1

    @api.multi
    def _get_numpy_date_unit(self):
        self.ensure_one()
        return "M"

    @api.multi
    @api.depends(
        "method_time",
        "method_number",
        "method_period",
        "depreciation_line_ids",
        "depreciation_line_ids.line_date",
    )
    def _compute_method_period_number(self):
        for asset in self:
            method_period_start_number = (
                method_period_depreciated_number
            ) = method_period_remaining_number = 0.0
            asset_value = asset.last_posted_asset_value_id
            depreciation = asset.last_depreciation_id

            coef_method_time = asset._get_method_time_coefficient()
            coef_method_period = asset._get_method_period_coefficient()
            method_period_number = (
                coef_method_time / coef_method_period
            ) * asset.method_number
            np_date_unit = asset._get_numpy_date_unit()

            dt_asset_start_date = np.datetime64(asset.date_start, np_date_unit)

            if asset_value:
                dt_posted_asset_value_date = np.datetime64(
                    asset_value.line_date, np_date_unit
                )
                dt_diff = dt_posted_asset_value_date - dt_asset_start_date
                method_period_start_number = int(dt_diff / coef_method_period)

            if depreciation and asset_value:
                # TODO: Pretty sure numpy has method to change string into dt
                dt_temp = datetime.strptime(asset_value.line_date, "%Y-%m-%d")
                dt_temp = dt_temp + relativedelta(day=1, days=-1)
                dt_temp = np.datetime64(dt_temp, np_date_unit)
                dt_depreciation = np.datetime64(depreciation.line_date, np_date_unit)
                method_period_depreciated_number = dt_depreciation - dt_temp

            method_period_remaining_number = (
                method_period_number
                - method_period_start_number
                - method_period_depreciated_number
            )

            asset.method_period_number = method_period_number
            asset.method_period_start_number = method_period_start_number
            asset.method_period_depreciated_number = method_period_depreciated_number
            asset.method_period_remaining_number = method_period_remaining_number

    method_period_number = fields.Integer(
        string="Age Based On Period Lenght",
        compute="_compute_method_period_number",
    )
    method_period_start_number = fields.Integer(
        string="Age On Asset Value Date",
        compute="_compute_method_period_number",
    )
    method_period_depreciated_number = fields.Integer(
        string="Depreciated Age",
        compute="_compute_method_period_number",
    )
    method_period_remaining_number = fields.Integer(
        string="Remaining Age",
        compute="_compute_method_period_number",
    )

    @api.multi
    def _prepare_valid_lines_domain(self):
        self.ensure_one()
        return [
            "&",
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _get_asset_value_line_domain(self):
        self.ensure_one()
        return [
            ("asset_id", "=", self.id),
            ("type", "=", "create"),
        ]

    @api.multi
    @api.depends(
        "depreciation_line_ids",
        "depreciation_line_ids.line_date",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_check",
        "depreciation_line_ids.type",
    )
    def _compute_last_posted_depreciation_line(self):
        obj_line = self.env["account.asset.depreciation.line"]
        for asset in self:
            criteria = asset._prepare_valid_lines_domain()
            lines = obj_line.search(criteria, order="type desc, line_date desc")
            line_id = False
            if len(lines) > 0:
                line_id = lines[0].id
            asset.last_posted_depreciation_line_id = line_id

            criteria = asset._get_asset_value_line_domain()
            lines = obj_line.search(criteria, order="line_date desc, type desc")
            line_id = False
            if len(lines) > 0:
                line_id = lines[0].id
            asset.last_posted_asset_line_id = line_id

    last_posted_depreciation_line_id = fields.Many2one(
        string="Last Posted Depreciation Line",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_last_posted_depreciation_line",
    )
    last_posted_asset_line_id = fields.Many2one(
        string="Last Asset Value Depreciation Line",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_last_posted_depreciation_line",
    )

    @api.multi
    def _prepare_posted_lines_domain(self):
        self.ensure_one()
        date = self.last_posted_asset_line_id.line_date
        return [
            "&",
            "&",
            "&",
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
            ("type", "=", "depreciate"),
            ("line_date", ">=", date),
            ("subtype_id", "=", False),
        ]

    @api.multi
    @api.depends(
        "depreciation_line_ids",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_check",
        "depreciation_line_ids.type",
    )
    def _compute_posted_depreciation_line_ids(self):
        obj_line = self.env["account.asset.depreciation.line"]
        for asset in self:
            domain = asset._prepare_posted_lines_domain()
            posted_lines = obj_line.search(domain, order="line_date desc")
            asset.posted_depreciation_line_ids = posted_lines.ids

    posted_depreciation_line_ids = fields.Many2many(
        string="Posted Depreciation Lines",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_posted_depreciation_line_ids",
    )

    @api.multi
    def _prepare_posted_asset_value_domain(self):
        self.ensure_one()
        return [
            ("type", "=", "create"),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_posted_depreciation_domain(self):
        self.ensure_one()
        return [
            "&",
            "&",
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
            ("type", "=", "depreciate"),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_posted_history_domain(self):
        self.ensure_one()
        return [
            "&",
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_unposted_history_domain(self):
        self.ensure_one()
        return [
            ("move_check", "=", False),
            ("init_entry", "=", False),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    @api.depends(
        "depreciation_line_ids",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_check",
        "depreciation_line_ids.type",
    )
    def _compute_asset_histories(self):
        obj_line = self.env["account.asset.depreciation.line"]
        for asset in self:
            last_posted_asset_value = (
                last_posted_depreciation
            ) = last_posted_history = False

            posted_asset_value_domain = asset._prepare_posted_asset_value_domain()
            posted_asset_values = obj_line.search(
                posted_asset_value_domain, order="line_date, type"
            )

            if len(posted_asset_values) > 0:
                last_posted_asset_value = posted_asset_values[-1]

            posted_depreciation_domain = asset._prepare_posted_depreciation_domain()
            posted_depreciations = obj_line.search(
                posted_depreciation_domain, order="line_date, type"
            )

            if len(posted_depreciations) > 0:
                last_posted_depreciation = posted_depreciations[-1]

            posted_history_domain = asset._prepare_posted_history_domain()
            posted_histories = obj_line.search(
                posted_history_domain, order="line_date, type"
            )

            if len(posted_histories) > 0:
                last_posted_history = posted_histories[-1]

            unposted_history_domain = asset._prepare_unposted_history_domain()
            unposted_histories = obj_line.search(
                unposted_history_domain, order="line_date, type"
            )

            asset.posted_asset_value_ids = posted_asset_values.ids
            asset.last_posted_asset_value_id = (
                last_posted_asset_value and last_posted_asset_value.id or False
            )
            asset.posted_depreciation_ids = posted_depreciations.ids
            asset.last_depreciation_id = (
                last_posted_depreciation and last_posted_depreciation.id or False
            )
            asset.unposted_history_ids = unposted_histories.ids
            asset.posted_history_ids = posted_histories.ids
            asset.last_posted_history_id = (
                last_posted_history and last_posted_history.id or False
            )

    posted_asset_value_ids = fields.Many2many(
        string="Posted Asset Value Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    last_posted_asset_value_id = fields.Many2one(
        string="Last Posted Asset Value History",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    posted_depreciation_ids = fields.Many2many(
        string="Posted Depreciation Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    last_depreciation_id = fields.Many2one(
        string="Last Depreciation History",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    unposted_history_ids = fields.Many2many(
        string="Unposted Asset Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    posted_history_ids = fields.Many2many(
        string="Posted Asset Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    last_posted_history_id = fields.Many2one(
        string="Last Posted History",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    prorate_by_month = fields.Boolean(
        string="Prorate by Month",
        default=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_min_prorate = fields.Integer(
        string="Date Min. to Prorate",
        default=15,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    open_date = fields.Datetime(
        string="Running Date",
        readonly=True,
        copy=False,
    )
    open_user_id = fields.Many2one(
        string="Running By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    close_date = fields.Datetime(
        string="Close Date",
        readonly=True,
        copy=False,
    )
    close_user_id = fields.Many2one(
        string="Close By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
    )

    @api.multi
    def _compute_policy(self):
        _super = super(AccountAssetAsset, self)
        _super._compute_policy()

    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    close_ok = fields.Boolean(
        string="Can Close",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
        store=False,
    )

    @api.model
    def create(self, vals):
        if vals.get("method_time") != "year" and not vals.get("prorata"):
            vals["prorata"] = True
        asset = super(AccountAssetAsset, self).create(vals)
        if self._context.get("create_asset_from_move_line"):
            asset.salvage_value = 0.0
        if asset.type == "normal":
            asset_line_obj = self.env["account.asset.depreciation.line"]
            line_name = asset._get_depreciation_entry_name(0)
            asset_date_start = asset._get_date_start()
            asset_line_vals = {
                "amount": asset.asset_value,
                "asset_id": asset.id,
                "name": line_name,
                "line_date": asset_date_start,
                "init_entry": True,
                "type": "create",
            }
            asset_line = asset_line_obj.create(asset_line_vals)
            if self._context.get("create_asset_from_move_line"):
                asset_line.move_id = self._context["move_id"]
        ctx = self.env.context.copy()
        ctx.update(
            {
                "ir_sequence_date": asset.date_start,
            }
        )
        sequence = asset.with_context(ctx)._create_sequence()
        asset.write(
            {
                "code": sequence,
            }
        )
        return asset

    @api.multi
    def write(self, vals):
        _super = super(AccountAssetAsset, self)
        res = _super.write(vals)
        context = self.env.context

        if vals.get("method_time"):
            if vals["method_time"] != "year" and not vals.get("prorata"):
                vals["prorata"] = True
        for asset in self:
            asset_type = vals.get("type") or asset.type

            if asset_type == "view" or context.get("asset_validate_from_write"):
                continue
            if asset.category_id.open_asset and context.get(
                "create_asset_from_move_line"
            ):
                asset.compute_depreciation_board()
                ctx = dict(context, asset_validate_from_write=True)
                asset.with_context(ctx).validate()
        return res

    @api.multi
    def unlink(self):
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(
                        _("Invalid action!"),
                        _("You can only delete data on draft state"),
                    )
            if document.account_move_line_ids:
                raise UserError(
                    _("Error!"),
                    _(
                        "You cannot delete an asset that contains "
                        "posted depreciation lines."
                    ),
                )
            parent = document.parent_id
            if parent:
                document.salvage_value = parent.salvage_value
        _super = super(AccountAssetAsset, self)
        _super.unlink()

    @api.multi
    def copy(self, default=None):
        _super = super(AccountAssetAsset, self)
        if default is None:
            default = {}
        update_vals = {
            "depreciation_line_ids": [],
            "account_move_line_ids": [],
            "state": "draft",
            "history_ids": [],
        }
        default.update(update_vals)

        return _super.copy(default)

    # -- Other Methods --
    @api.multi
    def _get_date_start(self):
        self.ensure_one()
        date_start = self.date_start
        dt_date_start = datetime.strptime(date_start, "%Y-%m-%d")
        if self.prorate_by_month:
            if dt_date_start.day > self.date_min_prorate:
                dt_date_start = dt_date_start + relativedelta(day=1, months=1)

        return dt_date_start.strftime("%Y-%m-%d")

    @api.multi
    def _get_assets(self):
        asset_ids = []
        for asset in self:

            def _parent_get(record):
                asset_ids.append(record.id)
                if record.parent_id:
                    _parent_get(record.parent_id)

            _parent_get(asset)
        return asset_ids

    @api.multi
    def _get_assets_from_dl(self):
        self.ensure_one()
        asset_ids = []
        filter_dl_ids = self.depreciation_line_ids.filtered(
            lambda x: x.type in ["depreciate", "remove"] and (x.init_entry or x.move_id)
        )
        for dl in filter_dl_ids:
            res = []

            def _parent_get(record):
                res.append(record.id)
                if record.parent_id:
                    res.append(_parent_get(record.parent_id))

            _parent_get(dl.asset_id)
            for asset_id in res:
                if asset_id not in asset_ids:
                    asset_ids.append(asset_id)
        return asset_ids

    @api.model
    def _get_period(self):
        context = self.env.context
        ctx = dict(context or {}, account_period_prefer_normal=True)
        periods = self.env["account.period"].with_context(ctx).find()
        if periods:
            return periods[0]
        else:
            return False

    @api.multi
    def _get_first_period_amount(
        self, table, entry, depreciation_start_date, line_dates
    ):
        """
        Return prorata amount for Time Method "Year" in case of
        "Prorata Temporis"
        """
        amount = entry.get("period_amount")
        if self.prorata:
            dates = filter(lambda x: x <= entry["date_stop"], line_dates)
            full_periods = len(dates) - 1
            amount = entry["fy_amount"] - amount * full_periods
        return amount

    @api.multi
    def _get_depreciation_entry_name(self, seq):
        """use this method to customise the name of the accounting entry"""
        return (self.code or str(self.id)) + "/" + str(seq)

    @api.multi
    def _prepare_old_lines_domain(self):
        self.ensure_one()
        return [
            ("asset_id", "=", self.id),
            ("type", "=", "depreciate"),
            ("move_id", "=", False),
            ("init_entry", "=", False),
        ]

    @api.multi
    def _delete_unposted_history(self):
        self.ensure_one()
        line_obj = self.env["account.asset.depreciation.line"]
        domain = self._prepare_old_lines_domain()
        old_lines = line_obj.search(domain)
        if old_lines:
            old_lines.unlink()

    @api.multi
    def _compute_starting_depreciation_entry(self, table):
        self.ensure_one()
        # TODO: Use new helper field
        line_obj = self.env["account.asset.depreciation.line"]
        domain = self._prepare_posted_lines_domain()
        posted_lines = line_obj.search(domain, order="line_date desc")

        # TODO: Use new helper field
        last_line = self.last_posted_depreciation_line_id

        if len(posted_lines) > 0:
            last_depreciation_date = datetime.strptime(last_line.line_date, "%Y-%m-%d")
            last_date_in_table = table[-1]["lines"][-1]["date"]
            if last_date_in_table <= last_depreciation_date:
                raise UserError(
                    _(
                        "The duration of the asset conflicts with the "
                        "posted depreciation table entry dates."
                    )
                )

            for _table_i, entry in enumerate(table):
                # residual_amount_table = \
                #     entry["lines"][-1]["remaining_value"]
                if entry["date_start"] <= last_depreciation_date <= entry["date_stop"]:
                    break
            if entry["date_stop"] == last_depreciation_date:
                _table_i += 1
                _line_i = 0
            else:
                entry = table[_table_i]
                date_min = entry["date_start"]
                for _line_i, line in enumerate(entry["lines"]):
                    # residual_amount_table = line["remaining_value"]
                    if date_min <= last_depreciation_date <= line["date"]:
                        break
                    date_min = line["date"]
                if line["date"] == last_depreciation_date:
                    _line_i += 1
            table_i_start = _table_i
            line_i_start = _line_i
        else:  # no posted lines
            table_i_start = 0
            line_i_start = 0

        return table_i_start, line_i_start

    @api.multi
    def _create_depreciation_lines(self, table, table_index_start, line_index_start):
        self.ensure_one()
        line_i_start = line_index_start
        table_i_start = table_index_start
        posted_lines = self.posted_depreciation_line_ids
        obj_line = self.env["account.asset.depreciation.line"]
        seq = len(posted_lines)
        # SPONGE
        depr_line = self.last_posted_history_id
        # depr_line = self.last_posted_depreciation_line_id

        # last_date = table[-1]["lines"][-1]["date"]
        depreciated_value = sum(vari_l.amount for vari_l in posted_lines)

        for entry in table[table_i_start:]:
            for line in entry["lines"][line_i_start:]:
                seq += 1
                name = self._get_depreciation_entry_name(seq)
                amount = line["amount"]

                if amount:
                    vals = {
                        "previous_id": depr_line.id,
                        "amount": amount,
                        "asset_id": self.id,
                        "name": name,
                        "line_date": line["date"].strftime("%Y-%m-%d"),
                        "init_entry": entry["init"],
                    }
                    depreciated_value += amount
                    depr_line = obj_line.create(vals)
                else:
                    seq -= 1
            line_i_start = 0

    @api.multi
    def compute_depreciation_board(self):
        for asset in self:
            if asset.value_residual == 0.0:
                continue
            asset._delete_unposted_history()
            table = asset._compute_depreciation_table()
            if not table:
                continue
            table_i_start, line_i_start = asset._compute_starting_depreciation_entry(
                table
            )
            asset._create_depreciation_lines(table, table_i_start, line_i_start)
        return True

    @api.multi
    def _get_depreciation_start_date(self, fy):
        """
        In case of "Linear": the first month is counted as a full month
        if the fiscal year starts in the middle of a month.
        """
        if self.prorata:
            depreciation_start_date = datetime.strptime(
                self.last_posted_asset_line_id.line_date, "%Y-%m-%d"
            )
            depreciation_start_date += relativedelta(day=1)
        else:
            fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
            depreciation_start_date = datetime(
                fy_date_start.year, fy_date_start.month, 1
            )
        return depreciation_start_date

    @api.multi
    def _get_depreciation_stop_date(self, depreciation_start_date):
        self.ensure_one()
        asset_start_date = datetime.strptime(self.date_start, "%Y-%m-%d")
        asset_start_date += relativedelta(day=1)
        if self.method_time == "year":
            depreciation_stop_date = asset_start_date + relativedelta(
                years=self.method_number, days=-1
            )
        elif self.method_time == "month":
            depreciation_stop_date = asset_start_date + relativedelta(
                months=self.method_number, days=-1
            )
        return depreciation_stop_date

    @api.multi
    def _get_amount_to_depreciate(self):
        self.ensure_one()
        asset_value = self.last_posted_asset_line_id.remaining_value
        if self.method == "linear":
            return asset_value - self.salvage_value
        else:
            return asset_value

    @api.multi
    def _compute_line_dates(self, table, start_date, stop_date):
        """
        The posting dates of the accounting entries depend on the
        chosen 'Period Length' as follows:
        - month: last day of the month
        - quarter: last of the quarter
        - year: last day of the fiscal year

        Override this method if another posting date logic is required.
        """
        line_dates = []

        if self.method_period == "month":
            line_date = start_date + relativedelta(day=31)
        if self.method_period == "quarter":
            m = [x for x in [3, 6, 9, 12] if x >= start_date.month][0]
            line_date = start_date + relativedelta(month=m, day=31)
        elif self.method_period == "year":
            line_date = table[0]["date_stop"]

        i = 1
        while line_date < stop_date:
            line_dates.append(line_date)
            if self.method_period == "month":
                line_date = line_date + relativedelta(months=1, day=31)
            elif self.method_period == "quarter":
                line_date = line_date + relativedelta(months=3, day=31)
            elif self.method_period == "year":
                line_date = table[i]["date_stop"]
                i += 1

        # last entry
        if not (self.method_time == "number" and len(line_dates) == self.method_number):
            line_dates.append(line_date)

        return line_dates

    @api.multi
    def _compute_year_amount(self, amount_to_depr, residual_amount):
        """
        Localization: override this method to change the degressive-linear
        calculation logic according to local legislation.
        """
        # if self.method_time != "year":
        #     raise UserError(
        #         _("Programming Error"),
        #         _(
        #             "The '_compute_year_amount' method is only intended for "
        #             "Time Method 'Number of Years.''"
        #         ),
        #     )

        if self.method_time in ["year", "month"]:
            year_amount_liner_divider = (
                self.method_period_number - self.method_period_start_number
            )
            year_amount_linear = (amount_to_depr / year_amount_liner_divider) * 12

        if self.method == "linear":
            return year_amount_linear

        year_amount_degressive = residual_amount * self.method_progress_factor

        if self.method == "degressive":
            return year_amount_degressive

        if self.method == "degr-linear":
            if year_amount_linear > year_amount_degressive:
                return min(year_amount_linear, residual_amount)
            else:
                return min(year_amount_degressive, residual_amount)

        raise UserError(_("Illegal value %s in asset.method.") % self.method)

    @api.model
    def _get_fy_duration_factor(self, entry, asset, firstyear):
        """
        localization: override this method to change the logic used to
        calculate the impact of extended/shortened fiscal years
        """
        duration_factor = 1.0
        fy_id = entry["fy_id"]
        if asset.prorata:
            if firstyear:
                depreciation_date_start = datetime.strptime(
                    asset.last_posted_asset_line_id.line_date, "%Y-%m-%d"
                )
                first_fy_asset_days = depreciation_date_start + relativedelta(day=1)

                duration_factor = float(13 - first_fy_asset_days.month) / 12.0

            elif fy_id:
                duration_factor = asset._get_fy_duration(fy_id, option="years")
        elif fy_id:
            fy_months = asset._get_fy_duration(fy_id, option="months")
            duration_factor = float(fy_months) / 12
        return duration_factor

    @api.model
    def _get_fy_duration(self, fy_id, option="days"):
        """
        Returns fiscal year duration.
        @param option:
        - days: duration in days
        - months: duration in months,
                  a started month is counted as a full month
        - years: duration in calendar years, considering also leap years
        """
        fy = self.env["account.fiscalyear"].browse(fy_id)
        fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
        fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
        days = (fy_date_stop - fy_date_start).days + 1
        months = (
            (fy_date_stop.year - fy_date_start.year) * 12
            + (fy_date_stop.month - fy_date_start.month)
            + 1
        )
        if option == "days":
            return days
        elif option == "months":
            return months
        elif option == "years":
            year = fy_date_start.year
            cnt = fy_date_stop.year - fy_date_start.year + 1
            for i in range(cnt):
                cy_days = calendar.isleap(year) and 366 or 365
                if i == 0:  # first year
                    if fy_date_stop.year == year:
                        duration = (fy_date_stop - fy_date_start).days + 1
                    else:
                        duration = (datetime(year, 12, 31) - fy_date_start).days + 1
                    factor = float(duration) / cy_days
                elif i == cnt - 1:  # last year
                    duration = (fy_date_stop - datetime(year, 1, 1)).days + 1
                    factor += float(duration) / cy_days
                else:
                    factor += 1.0
                year += 1
            return factor

    @api.multi
    def _compute_depreciation_table_lines(
        self, table, depreciation_start_date, depreciation_stop_date, line_dates
    ):

        digits = self.env["decimal.precision"].precision_get("Asset Depreciation")
        asset_sign = self._get_asset_value() >= 0 and 1 or -1
        i_max = len(table) - 1
        remaining_value = self._get_amount_to_depreciate()
        depreciated_value = 0.0

        # raise UserError(str(table))

        for i, entry in enumerate(table):

            lines = []
            fy_amount_check = 0.0
            fy_amount = entry["fy_amount"]
            li_max = len(line_dates) - 1
            for li, line_date in enumerate(line_dates):

                if round(remaining_value, digits) == 0.0:
                    break

                if line_date > min(entry["date_stop"], depreciation_stop_date) and not (
                    i == i_max and li == li_max
                ):
                    break

                if (
                    self.method == "degr-linear"
                    and asset_sign * (fy_amount - fy_amount_check) < 0
                ):
                    break

                amount = entry.get("period_amount")

                # last year, last entry
                # Handle rounding deviations.
                if i == i_max and li == li_max:
                    amount = remaining_value
                    remaining_value = 0.0
                else:
                    remaining_value -= amount

                fy_amount_check += amount
                line = {
                    "date": line_date,
                    "amount": amount,
                    "depreciated_value": depreciated_value,
                    "remaining_value": remaining_value,
                }
                lines.append(line)
                depreciated_value += amount

            # Handle rounding and extended/shortened FY deviations.
            #
            # Remark:
            # In account_asset_management version < 8.0.2.8.0
            # the FY deviation for the first FY
            # was compensated in the first FY depreciation line.
            # The code has now been simplified with compensation
            # always in last FT depreciation line.

            if round(fy_amount_check - fy_amount, digits) != 0:
                diff = fy_amount_check - fy_amount
                amount = amount - diff
                remaining_value += diff
                lines[-1].update(
                    {
                        "amount": amount,
                        "remaining_value": remaining_value,
                    }
                )
                depreciated_value -= diff

            if not lines:
                table.pop(i)
            else:
                entry["lines"] = lines
            line_dates = line_dates[li:]

        for _i, entry in enumerate(table):
            if not entry["fy_amount"]:
                entry["fy_amount"] = sum(var_l["amount"] for var_l in entry["lines"])

    @api.multi
    def _compute_depreciation_table(self):  # noqa: C901
        ctx = self._context.copy()

        table = []
        if self.method_time in ["year", "number"] and not self.method_number:
            return table

        ctx["company_id"] = self.company_id.id
        fy_obj = self.env["account.fiscalyear"].with_context(ctx)
        init_flag = False
        try:
            # SPONGE
            fy_id = fy_obj.find(self.last_posted_asset_line_id.line_date)
            # fy_id = fy_obj.find(self.date_start)
            fy = fy_obj.browse(fy_id)
            if fy.state == "done":
                init_flag = True
            fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
            fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
        except:  # noqa: E722
            # The following logic is used when no fiscal year
            # is defined for the asset start date:
            # - We lookup the first fiscal year defined in the system
            # - The "undefined" fiscal years are assumed to be years
            #   with a duration equal to a calendar year
            first_fy = fy_obj.search(
                [("company_id", "=", self.company_id.id)],
                order="date_stop ASC",
                limit=1,
            )
            first_fy_date_start = datetime.strptime(first_fy.date_start, "%Y-%m-%d")
            # SPONGE
            asset_date_start = datetime.strptime(
                self.last_posted_asset_line_id.line_date, "%Y-%m-%d"
            )
            fy_date_start = first_fy_date_start
            if asset_date_start > fy_date_start:
                asset_ref = (
                    self.code
                    and "{} (ref: {})".format(self.name, self.code)
                    or self.name
                )
                raise UserError(
                    _(
                        "You cannot compute a depreciation table for an asset "
                        "starting in an undefined future fiscal year."
                        "\nPlease correct the start date for asset %s."
                    )
                    % asset_ref
                )
            while asset_date_start < fy_date_start:
                fy_date_start = fy_date_start - relativedelta(years=1)
            fy_date_stop = fy_date_start + relativedelta(years=1, days=-1)
            fy_id = False
            fy = DummyFy(
                date_start=fy_date_start.strftime("%Y-%m-%d"),
                date_stop=fy_date_stop.strftime("%Y-%m-%d"),
                id=False,
                state="done",
                dummy=True,
            )
            init_flag = True

        depreciation_start_date = self._get_depreciation_start_date(fy)
        depreciation_stop_date = self._get_depreciation_stop_date(
            depreciation_start_date
        )

        while fy_date_start <= depreciation_stop_date:
            table.append(
                {
                    "fy_id": fy_id,
                    "date_start": fy_date_start,
                    "date_stop": fy_date_stop,
                    "init": init_flag,
                }
            )
            fy_date_start = fy_date_stop + relativedelta(days=1)
            try:
                fy_id = fy_obj.find(fy_date_start)
                init_flag = False
            except:  # noqa : E722
                fy_id = False
            if fy_id:
                fy = fy_obj.browse(fy_id)
                if fy.state == "done":
                    init_flag = True
                fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
            else:
                fy_date_stop = fy_date_stop + relativedelta(years=1)

        # Step 1:
        # Calculate depreciation amount per fiscal year.
        # This is calculation is skipped for method_time != "year".
        obj_dp = self.env["decimal.precision"]
        digits = obj_dp.precision_get("Asset Depreciation")
        fy_residual_amount = amount_to_depr = self._get_amount_to_depreciate()

        i_max = len(table) - 1
        asset_sign = self._get_asset_value() >= 0 and 1 or -1

        line_dates = self._compute_line_dates(
            table, depreciation_start_date, depreciation_stop_date
        )

        for i, entry in enumerate(table):

            year_amount = self._compute_year_amount(amount_to_depr, fy_residual_amount)

            if i == i_max:
                if self.method == "degressive":
                    year_amount = fy_residual_amount - self.salvage_value

            if self.method_period == "year":
                period_amount = year_amount
            elif self.method_period == "quarter":
                period_amount = year_amount / 4
            elif self.method_period == "month":
                period_amount = year_amount / 12

            if i == i_max:
                if self.method == "linear":
                    fy_amount = fy_residual_amount
                else:
                    fy_amount = fy_residual_amount - self.salvage_value
            else:
                firstyear = i == 0 and True or False
                fy_factor = self._get_fy_duration_factor(entry, self, firstyear)

                fy_amount = year_amount * fy_factor

            if asset_sign * (fy_amount - fy_residual_amount) > 0:
                fy_amount = fy_residual_amount

            period_amount = round(period_amount, digits)
            fy_amount = round(fy_amount, digits)

            entry.update(
                {
                    "period_amount": period_amount,
                    "fy_amount": fy_amount,
                }
            )

            fy_residual_amount -= fy_amount
            if round(fy_residual_amount, digits) == 0:
                break

        i_max = i
        table = table[: i_max + 1]

        # Step 2:
        # Spread depreciation amount per fiscal year
        # over the depreciation periods.
        self._compute_depreciation_table_lines(
            table, depreciation_start_date, depreciation_stop_date, line_dates
        )

        return table

    @api.multi
    def _compute_entries(self, period_id, check_triggers=False):
        # To DO : add ir_cron job calling this method to
        # generate periodical accounting entries
        context = self.env.context
        result = []
        obj_depreciation_line = self.env["account.asset.depreciation.line"]
        # period = period_id
        if check_triggers:
            obj_asset_recompute = self.env["account.asset.recompute.trigger"]
            recompute_ids = obj_asset_recompute.sudo().search([("state", "=", "open")])
            if recompute_ids:
                recompute_triggers = recompute_ids.read(["company_id"])

        # assets = self.browse(cr, uid, ids, context=context)
        for asset in self:
            criteria_1 = [
                ("asset_id", "=", asset.id),
                ("type", "=", "depreciate"),
                ("init_entry", "=", False),
                ("line_date", "<", period_id.date_start),
                ("move_check", "=", False),
            ]
            depreciation_ids = obj_depreciation_line.search(criteria_1)
            if depreciation_ids:
                for _line in depreciation_ids:
                    asset_ref = (
                        asset.code
                        and "{} (ref: {})".format(asset.name, asset.code)
                        or asset.name
                    )
                    raise UserError(
                        _("Error!"),
                        _(
                            "Asset '%s' contains unposted lines "
                            "prior to the selected period."
                            "\nPlease post these entries first !"
                        )
                        % asset_ref,
                    )
            if check_triggers and recompute_ids:
                triggers = filter(
                    lambda x: x["company_id"][0] == asset.company_id.id,
                    recompute_triggers,
                )
                if triggers:
                    asset.compute_depreciation_board()
        criteria_2 = [
            ("asset_id", "in", self.ids),
            ("type", "=", "depreciate"),
            ("init_entry", "=", False),
            ("line_date", "<=", period_id.date_stop),
            ("line_date", ">=", period_id.date_start),
            ("move_check", "=", False),
        ]
        depreciation_ids = obj_depreciation_line.search(criteria_2)
        for depreciation in depreciation_ids:
            context.update({"depreciation_date": depreciation.line_date})
            result += depreciation.with_context(context).create_move()

        if check_triggers and recompute_ids:
            asset_company_ids = {x.company_id.id for x in self}
            triggers = filter(
                lambda x: x["company_id"][0] in asset_company_ids, recompute_triggers
            )
            if triggers:
                recompute_vals = {
                    "date_completed": time.strftime(
                        tools.DEFAULT_SERVER_DATETIME_FORMAT
                    ),
                    "state": "done",
                }
                trigger_ids = [x["id"] for x in triggers]
                trigger_ids.sudo().write(recompute_vals)
        return result

    # -- Constrains Methods --
    @api.constrains(
        "method",
        "method_time",
    )
    def _check_method(self):
        str_error = _("Degressive-Linear is only supported for Time Method = Year.")
        if self.method == "degr-linear" and self.method_time != "year":
            raise UserError(str_error)

    # -- Onchange Methods --
    @api.onchange(
        "category_id",
    )
    def onchange_category_id(self):
        if not self._context.get("create_asset_from_move_line"):
            if self.depreciation_line_ids:
                for line in self.depreciation_line_ids:
                    if line.move_id:
                        raise UserError(
                            _("Error!"),
                            _(
                                "You cannot change the category of an asset "
                                "with accounting entries."
                            ),
                        )
        obj_asset_category = self.env["account.asset.category"]
        if self.category_id:
            category = obj_asset_category.browse(self.category_id.id)
            self.method = category.method
            self.method_number = category.method_number
            self.method_time = category.method_time
            self.method_period = category.method_period
            self.method_progress_factor = category.method_progress_factor
            self.prorata = category.prorata
            self.account_analytic_id = category.account_analytic_id.id

    @api.onchange(
        "category_id",
    )
    def onchange_date_min_prorate(self):
        self.date_min_prorate = False
        if self.category_id:
            self.date_min_prorate = self.category_id.date_min_prorate

    @api.onchange(
        "asset_value",
    )
    def onchange_amount_depreciation_line(self):
        dl_ids = self.depreciation_line_ids.filtered(lambda x: x.type == "create")
        if dl_ids:
            for document in dl_ids:
                document.amount = self.asset_value

    @api.onchange(
        "date_start",
    )
    def onchange_line_date_depreciation_line(self):
        dl_ids = self.depreciation_line_ids.filtered(lambda x: x.type == "create")
        if dl_ids:
            for document in dl_ids:
                document.line_date = self.date_start

    @api.onchange(
        "method_time",
    )
    def onchange_method_time(self):
        if self.method_time != "year":
            self.prorata = True

    @api.onchange(
        "type",
    )
    def onchange_type_date_start(self):
        if self.type == "view":
            self.date_start = False

    @api.onchange(
        "type",
    )
    def onchange_type_category_id(self):
        if self.type == "view":
            self.category_id = False

    @api.onchange(
        "type",
    )
    def onchange_type_purchase_value(self):
        if self.type == "view":
            self.purchase_value = 0.0

    @api.onchange(
        "type",
    )
    def onchange_type_salvage_value(self):
        if self.type == "view":
            self.salvage_value = 0.0

    @api.onchange(
        "type",
    )
    def onchange_type_code(self):
        if self.type == "view":
            self.code = False

    @api.onchange(
        "type",
    )
    def onchange_type_depreciation_line_ids(self):
        if self.depreciation_line_ids:
            self.depreciation_line_ids.unlink()

    # -- Workflow Methods --
    @api.multi
    def validate_tier(self):
        _super = super(AccountAssetAsset, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.validate()

    @api.multi
    def restart_validation(self):
        _super = super(AccountAssetAsset, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        return {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }

    @api.multi
    def validate(self):
        for document in self:
            currency = document.company_id.currency_id
            if document.type == "normal" and currency.is_zero(document.value_residual):
                document.write(document._prepare_close_data())
            else:
                document.write(document._prepare_open_data())

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "open_date": False,
            "open_user_id": False,
        }

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def action_cancel(self):
        for document in self:
            dl_ids = document.depreciation_line_ids.filtered(
                lambda x: x.type != "create"
            )
            if dl_ids:
                dl_ids.unlink()
            document.write(document._prepare_cancel_data())

    @api.multi
    def remove(self):
        for document in self:
            ctx = {}
            if document.value_residual:
                ctx.update({"early_removal": True})
        return {
            "name": _("Generate Asset Removal entries"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": "account.asset.remove",
            "target": "new",
            "type": "ir.actions.act_window",
            "context": ctx,
            "nodestroy": True,
        }

    @api.multi
    def _prepare_close_data(self):
        self.ensure_one()
        return {
            "state": "close",
            "close_date": fields.Datetime.now(),
            "close_user_id": self.env.user.id,
        }

    @api.multi
    def _get_account_move_ids(self):
        return self.mapped("account_move_line_ids.move_id")

    @api.multi
    def _get_action_account_move(self):
        action = self.env.ref("account." "action_move_journal_line").read()[0]
        return action

    @api.multi
    def open_entries(self):
        self.ensure_one()
        account_move_ids = self._get_account_move_ids()
        action = self._get_action_account_move()

        if len(account_move_ids) > 0:
            action["domain"] = [("id", "in", account_move_ids.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action
