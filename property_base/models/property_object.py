# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PropertyObject(models.Model):
    _name = "property.object"
    _description = "Common Class for Property Object"

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_allowed_parent_type_ids(self):
        for document in self:
            result = []
            if document.type_id:
                result = document.type_id.allowed_parent_type_ids.ids
            document.allowed_parent_type_ids = result

    @api.multi
    @api.depends(
        "type_id",
        "parent_id",
    )
    def _compute_full_name(self):
        for document in self:
            address_format = document.type_id.display_name_format or \
                "%(name)s"
            args = {
                "name": document.name,
                "parent_name": document.parent_id.full_name,
                "parent_full_name": document.parent_id.full_name,
            }
            document.full_name = address_format % args

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_need_parent(self):
        for document in self:
            document.need_parent = document.type_id.need_parent

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_occupy_ok(self):
        for document in self:
            document.occupy_ok = document.type_id.occupy_ok

    name = fields.Char(
        string="Property",
        required=True,
    )
    full_name = fields.Char(
        string="Full Name",
        compute="_compute_full_name",
        store=False,
    )
    note = fields.Text(
        string="Notes"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
    parent_id = fields.Many2one(
        string="Parent Property",
        comodel_name="property.object",
    )
    occupy_ok = fields.Boolean(
        string="Can Be Occupied",
        compute="_compute_occupy_ok",
        store=False,
    )
    need_parent = fields.Boolean(
        string="Need Parent",
        compute="_compute_need_parent",
        store=False,
    )
    child_ids = fields.One2many(
        string="Child Properties",
        comodel_name="property.object",
        inverse_name="parent_id",
    )
    allowed_parent_type_ids = fields.Many2many(
        string="Allowed Parent Types",
        comodel_name="property.object_type",
        compute="_compute_allowed_parent_type_ids",
        store=False,
    )
    partner_id = fields.Many2one(
        string="Owner",
        comodel_name="res.partner",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="property.object_type",
    )
    size = fields.Float(
        string="Property Size",
    )
    size_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    owner_id = fields.Many2one(
        string="Owner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
    )
    tenant_id = fields.Many2one(
        string="Occupant",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
    )
    tenacy_status_id = fields.Many2one(
        string="Occupancy Status",
        comodel_name="property.tenacy_status",
    )
    availability_status_id = fields.Many2one(
        string="Availability Status",
        comodel_name="property.availability_status",
    )
    product_id = fields.Many2one(
        string="Product Link",
        comodel_name="product.product",
    )

    @api.onchange(
        "type_id",
    )
    def onchange_parent_id(self):
        self.parent_id = False

    @api.multi
    def name_get(self):
        result = []
        for document in self:
            result.append((document.id, document.full_name))
        return result
